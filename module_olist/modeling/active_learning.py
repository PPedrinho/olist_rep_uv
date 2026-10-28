import os
from pathlib import Path

os.environ.setdefault("KERAS_BACKEND", "tensorflow")

import keras
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


SEED = 42
POOL_SIZE = 8000
INITIAL_LABELS = 200
QUERIES_PER_ROUND = 200
ROUNDS = 5
EPOCHS = 4
BATCH_SIZE = 64

OUTPUT_DIR = Path("reports")
RESULTS_PATH = OUTPUT_DIR / "active_learning_keras.csv"
FIGURE_PATH = OUTPUT_DIR / "active_learning_keras.png"


def load_data():
    (x_train, y_train), (x_test, y_test) = keras.datasets.mnist.load_data()

    x_train = x_train.astype("float32") / 255.0
    x_test = x_test.astype("float32") / 255.0

    x_train = np.expand_dims(x_train, axis=-1)
    x_test = np.expand_dims(x_test, axis=-1)

    rng = np.random.default_rng(SEED)
    selected = rng.choice(len(x_train), size=POOL_SIZE, replace=False)

    return (
        x_train[selected],
        y_train[selected],
        x_test,
        y_test,
    )


def create_model():
    model = keras.Sequential(
        [
            keras.layers.Input(shape=(28, 28, 1)),
            keras.layers.Conv2D(32, 3, activation="relu"),
            keras.layers.MaxPooling2D(),
            keras.layers.Conv2D(64, 3, activation="relu"),
            keras.layers.MaxPooling2D(),
            keras.layers.Flatten(),
            keras.layers.Dense(128, activation="relu"),
            keras.layers.Dropout(0.3),
            keras.layers.Dense(10, activation="softmax"),
        ]
    )

    model.compile(
        optimizer=keras.optimizers.Adam(learning_rate=1e-3),
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"],
    )

    return model


def initial_indices(labels):
    rng = np.random.default_rng(SEED)
    chosen = []

    for class_id in range(10):
        candidates = np.flatnonzero(labels == class_id)
        chosen.append(rng.choice(candidates))

    remaining = np.setdiff1d(np.arange(len(labels)), chosen)
    extra = rng.choice(
        remaining,
        size=INITIAL_LABELS - len(chosen),
        replace=False,
    )

    return np.concatenate([np.array(chosen), extra])


def entropy_sampling(probabilities, candidates, n_queries):
    selected_probabilities = probabilities[candidates]
    safe_probabilities = np.clip(selected_probabilities, 1e-10, 1.0)
    entropy = -np.sum(
        safe_probabilities * np.log(safe_probabilities),
        axis=1,
    )

    order = np.argsort(entropy)[::-1]
    return candidates[order[:n_queries]]


def train_round(x_pool, y_pool, labeled_mask, x_test, y_test):
    model = create_model()

    x_labeled = x_pool[labeled_mask]
    y_labeled = y_pool[labeled_mask]

    model.fit(
        x_labeled,
        y_labeled,
        validation_split=0.15,
        epochs=EPOCHS,
        batch_size=BATCH_SIZE,
        verbose=0,
        callbacks=[
            keras.callbacks.EarlyStopping(
                monitor="val_loss",
                patience=1,
                restore_best_weights=True,
            )
        ],
    )

    loss, accuracy = model.evaluate(
        x_test,
        y_test,
        batch_size=256,
        verbose=0,
    )

    probabilities = model.predict(
        x_pool,
        batch_size=256,
        verbose=0,
    )

    return model, probabilities, float(loss), float(accuracy)


def run_strategy(
    x_pool,
    y_pool,
    x_test,
    y_test,
    strategy,
    initial_mask,
):
    rng = np.random.default_rng(SEED)
    labeled_mask = initial_mask.copy()
    history = []

    for round_id in range(ROUNDS + 1):
        _, probabilities, loss, accuracy = train_round(
            x_pool,
            y_pool,
            labeled_mask,
            x_test,
            y_test,
        )

        history.append(
            {
                "strategy": strategy,
                "round": round_id,
                "labeled_samples": int(labeled_mask.sum()),
                "test_loss": loss,
                "test_accuracy": accuracy,
            }
        )

        if round_id == ROUNDS:
            break

        candidates = np.flatnonzero(~labeled_mask)
        n_queries = min(QUERIES_PER_ROUND, len(candidates))

        if strategy == "uncertainty":
            queries = entropy_sampling(
                probabilities,
                candidates,
                n_queries,
            )
        elif strategy == "random":
            queries = rng.choice(
                candidates,
                size=n_queries,
                replace=False,
            )
        else:
            raise ValueError(f"Estratégia inválida: {strategy}")

        labeled_mask[queries] = True

    return pd.DataFrame(history)


def plot_results(history):
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    figure, axis = plt.subplots(figsize=(8, 5))

    for strategy, group in history.groupby("strategy"):
        axis.plot(
            group["labeled_samples"],
            group["test_accuracy"],
            marker="o",
            label=strategy,
        )

    axis.set_xlabel("Amostras rotuladas")
    axis.set_ylabel("Acurácia no teste")
    axis.set_title("Active Learning com Keras")
    axis.legend()
    axis.grid(alpha=0.25)

    figure.tight_layout()
    figure.savefig(FIGURE_PATH, dpi=150)
    plt.close(figure)


def main():
    keras.utils.set_random_seed(SEED)

    print(f"Keras: {keras.__version__}")
    print("Carregando MNIST...")

    x_pool, y_pool, x_test, y_test = load_data()

    initial = initial_indices(y_pool)
    initial_mask = np.zeros(len(y_pool), dtype=bool)
    initial_mask[initial] = True

    histories = []

    for strategy in ("uncertainty", "random"):
        print(f"\nEstratégia: {strategy}")

        result = run_strategy(
            x_pool,
            y_pool,
            x_test,
            y_test,
            strategy,
            initial_mask,
        )

        histories.append(result)

        for row in result.itertuples(index=False):
            print(
                f"rodada={row.round} | "
                f"rotulados={row.labeled_samples} | "
                f"acurácia={row.test_accuracy:.4f}"
            )

    history = pd.concat(histories, ignore_index=True)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    history.to_csv(RESULTS_PATH, index=False)

    plot_results(history)

    print(f"\nResultados salvos em: {RESULTS_PATH}")
    print(f"Gráfico salvo em: {FIGURE_PATH}")


if __name__ == "__main__":
    main()
