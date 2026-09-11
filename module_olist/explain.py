import pandas as pd
import shap
import matplotlib.pyplot as plt

from loguru import logger

from module_olist.config import (
    FIGURES_DIR,
    INTERIM_DATA_DIR,
    MODELS_DIR
)

from module_olist.modeling.predict import (
    load_model,
)

from module_olist.modeling.interpret import (
    prepare_data_for_shap,
    create_explainer,
    calculate_shap_values,
)


def explain_model():

    logger.info(
        "Carregando modelo para interpretação..."
    )


    model, model_name, threshold = load_model(
        model_path=MODELS_DIR / "best_model.joblib",
        metadata_path=MODELS_DIR / "metadata.json"
    )


    data = pd.read_csv(
        INTERIM_DATA_DIR /
        "orders_dataset_refined.csv"
    )


    features = [
        "promised_days",
        "item_count",
        "seller_count",
        "total_price",
        "total_freight",
        "purchase_month",
        "purchase_weekday",
        "purchase_hour",
        "customer_state",
    ]


    X = data[features]


    X_sample = X.sample(
        n=200,
        random_state=42
    )


    logger.info(
        "Preparando dados para SHAP..."
    )


    X_transformed = prepare_data_for_shap(
        model,
        X_sample
    )


    explainer = create_explainer(
        model
    )


    shap_values = calculate_shap_values(
        explainer,
        X_transformed
    )


    FIGURES_DIR.mkdir(
        parents=True,
        exist_ok=True
    )


    plt.figure(
        figsize=(12,8)
    )


    shap.summary_plot(
        shap_values,
        X_transformed,
        show=False
    )


    plt.tight_layout()


    plt.savefig(
        FIGURES_DIR /
        "shap_summary.png",
        dpi=300,
        bbox_inches="tight"
    )


    plt.close()


    logger.success(
        "Gráfico SHAP salvo com sucesso"
    )


def main():

    explain_model()


if __name__ == "__main__":
    main()