import json
import joblib

import warnings

warnings.filterwarnings("ignore")

from loguru import logger

from module_olist.explain import explain_model

from module_olist.config import (
    RAW_DATA_DIR,
    INTERIM_DATA_DIR,
    MODELS_DIR
)


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

    logger.info(
        "Iniciando pipeline Olist..."
    )


    # ===============================
    # Preparação dos dados
    # ===============================

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


    data = create_features(
        data
    )


    save_dataset(
        data,
        INTERIM_DATA_DIR /
        "orders_dataset_refined.csv"
    )


    # ===============================
    # Split
    # ===============================

    X_train, X_test, y_train, y_test = split_data(
        data
    )


    # ===============================
    # Cross Validation
    # ===============================

    best_model_name, best_threshold = cross_validate_models(
        X_train,
        y_train
    )


    logger.success(
        f"Modelo escolhido: {best_model_name}"
    )

    logger.info(
        f"Threshold escolhido: {best_threshold:.2f}"
    )


    # ===============================
    # Treinamento final
    # ===============================

    models = train_models(
        X_train,
        y_train
    )


    final_model = models[
        best_model_name
    ]


    # ===============================
    # Salvar modelo
    # ===============================

    MODELS_DIR.mkdir(
        parents=True,
        exist_ok=True
    )


    model_path = (
        MODELS_DIR /
        "best_model.joblib"
    )


    metadata_path = (
        MODELS_DIR /
        "metadata.json"
    )


    joblib.dump(
        final_model,
        model_path
    )


    metadata = {
        "model_name": best_model_name,
        "threshold": float(best_threshold)
    }


    with open(
        metadata_path,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            metadata,
            file,
            indent=4
        )


    logger.success(
        "Modelo e metadata salvos com sucesso"
    )

    logger.info(
    "Iniciando interpretação do modelo..."
    )

    explain_model()

    logger.success(
        "Interpretação concluída!"
    )

    logger.success(
        "Treinamento finalizado!"
    )



if __name__ == "__main__":
    main()