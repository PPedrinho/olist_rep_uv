from loguru import logger
from sklearn.metrics import confusion_matrix

from module_olist.config import RAW_DATA_DIR, INTERIM_DATA_DIR

from module_olist.dataset import (
    load_data,
    create_dataset,
    save_dataset
)

from module_olist.features import create_features

from module_olist.modeling.split import split_data
from module_olist.modeling.train import train_models
from module_olist.modeling.evaluate import evaluate_models


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

    models = train_models(
        X_train,
        y_train
    )

    evaluate_models(
        models,
        X_test,
        y_test
    )

    model = models["LightGBM"]

    y_proba = model.predict_proba(X_test)[:, 1]

    y_pred = (y_proba >= 0.13).astype(int)

    TN, FP, FN, TP = confusion_matrix(
        y_test,
        y_pred
    ).ravel()

    logger.info(f"TN: {TN}")
    logger.info(f"FP: {FP}")
    logger.info(f"FN: {FN}")
    logger.info(f"TP: {TP}")


if __name__ == "__main__":
    main()