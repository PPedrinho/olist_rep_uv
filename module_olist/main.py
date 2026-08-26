from loguru import logger

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

    output_path = INTERIM_DATA_DIR / "orders_dataset_improved.csv"

    save_dataset(
        data,
        output_path
    )


if __name__ == "__main__":
    main()