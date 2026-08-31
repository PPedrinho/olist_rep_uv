import pandas as pd

from loguru import logger

from sklearn.model_selection import StratifiedKFold, cross_validate

from module_olist.modeling.pipeline import (
    create_gradient_boosting_pipeline,
    create_lightgbm_pipeline,
    create_xgboost_pipeline
)


def cross_validate_models(
    X_train: pd.DataFrame,
    y_train: pd.Series
):

    models = {
        "Gradient Boosting": create_gradient_boosting_pipeline(),
        "XGBoost": create_xgboost_pipeline(),
        "LightGBM": create_lightgbm_pipeline()
    }


    cv = StratifiedKFold(
        n_splits=5,
        shuffle=True,
        random_state=42
    )


    scoring = {
        "precision": "precision",
        "recall": "recall",
        "f1": "f1",
        "roc_auc": "roc_auc"
    }


    results = {}


    for name, model in models.items():

        logger.info(
            f"Iniciando Cross Validation: {name}"
        )


        scores = cross_validate(
            model,
            X_train,
            y_train,
            cv=cv,
            scoring=scoring,
            n_jobs=-1
        )


        results[name] = {
            "precision": scores["test_precision"].mean(),
            "recall": scores["test_recall"].mean(),
            "f1": scores["test_f1"].mean(),
            "roc_auc": scores["test_roc_auc"].mean()
        }


        logger.info(
            f"{name}"
        )

        logger.info(
            f"Precision: {results[name]['precision']:.3f}"
        )

        logger.info(
            f"Recall: {results[name]['recall']:.3f}"
        )

        logger.info(
            f"F1: {results[name]['f1']:.3f}"
        )

        logger.info(
            f"ROC-AUC: {results[name]['roc_auc']:.3f}"
        )


    return results