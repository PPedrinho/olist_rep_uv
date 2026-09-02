from loguru import logger
from sklearn.metrics import (
    confusion_matrix,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score
)

from module_olist.config import RAW_DATA_DIR, INTERIM_DATA_DIR

from module_olist.dataset import (
    load_data,
    create_dataset,
    save_dataset
)

from module_olist.features import create_features

from module_olist.modeling.split import split_data
from module_olist.modeling.train import train_models
from module_olist.modeling.cross_validation import cross_validate_models


def main():

    logger.info("Iniciando preparação dos dados...")

    orders, items, customers = load_data(
        orders_path=RAW_DATA_DIR / "olist_orders_dataset.csv",
        items_path=RAW_DATA_DIR / "olist_order_items_dataset.csv",
        customers_path=RAW_DATA_DIR / "olist_customers_dataset.csv"
    )

    data = create_dataset(
        orders,
        items,
        customers
    )

    data = create_features(data)

    save_dataset(
        data,
        INTERIM_DATA_DIR / "orders_dataset_improved.csv"
    )

    X_train, X_test, y_train, y_test = split_data(data)

    best_model_name, best_threshold = cross_validate_models(
        X_train,
        y_train
    )

    logger.success(
        f"Modelo selecionado pela Cross Validation: {best_model_name}"
    )

    logger.info(
        f"Threshold selecionado: {best_threshold:.2f}"
    )

    models = train_models(
        X_train,
        y_train
    )

    model = models[best_model_name]

    y_proba = model.predict_proba(
        X_test
    )[:, 1]

    y_pred = (
        y_proba >= best_threshold
    ).astype(int)

    precision = precision_score(
        y_test,
        y_pred,
        zero_division=0
    )

    recall = recall_score(
        y_test,
        y_pred,
        zero_division=0
    )

    f1 = f1_score(
        y_test,
        y_pred,
        zero_division=0
    )

    roc_auc = roc_auc_score(
        y_test,
        y_proba
    )

    TN, FP, FN, TP = confusion_matrix(
        y_test,
        y_pred
    ).ravel()

    logger.info("AVALIAÇÃO FINAL NO TESTE")

    logger.info(
        f"Modelo: {best_model_name}"
    )

    logger.info(
        f"Threshold: {best_threshold:.2f}"
    )

    logger.info(
        f"Precision: {precision:.3f}"
    )

    logger.info(
        f"Recall: {recall:.3f}"
    )

    logger.info(
        f"F1: {f1:.3f}"
    )

    logger.info(
        f"ROC-AUC: {roc_auc:.3f}"
    )

    logger.info(
        f"TN: {TN}"
    )

    logger.info(
        f"FP: {FP}"
    )

    logger.info(
        f"FN: {FN}"
    )

    logger.info(
        f"TP: {TP}"
    )

    logger.success(
        "Pipeline executado com sucesso"
    )


if __name__ == "__main__":
    main()