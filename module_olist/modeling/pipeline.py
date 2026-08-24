from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.ensemble import GradientBoostingClassifier
from xgboost import XGBClassifier
from lightgbm import LGBMClassifier

NUMERIC_FEATURES = [
    "promised_days",
    "item_count",
    "seller_count",
    "total_price",
    "total_freight",
]

CATEGORICAL_FEATURES = [
    "purchase_hour",
    "purchase_weekday",
    "purchase_month",
    "customer_state",
]

def create_preprocessor() -> ColumnTransformer:

    return ColumnTransformer(
        transformers=[
            ("numeric", "passthrough", NUMERIC_FEATURES),
            ("categorical", OneHotEncoder(handle_unknown="ignore"), CATEGORICAL_FEATURES),
        ]    
    )

def create_gradient_boosting_pipeline() -> Pipeline:

    preprocessador = create_preprocessor()

    model = GradientBoostingClassifier(
        n_estimators=100,  # n° de árvores 
        learning_rate=0.1, # taxa de aprendizaado
        max_depth=3,       # profundidade
        random_state=42    # semente para reproduzibilidade
    )

    return Pipeline(
        steps=[("preprocessor", preprocessador), 
               ("model", model)]
    )

def create_xgboost_pipeline() -> Pipeline:
    preprocessador = create_preprocessor()

    model = XGBClassifier(
        n_estimators=100,  # n° de árvores 
        learning_rate=0.1, # taxa de aprendizaado
        max_depth=3,       # profundidade
        random_state=42    # semente para reproduzibilidade
    )

    return Pipeline(
        steps=[("preprocessor", preprocessador), 
               ("model", model)]
    )

def create_lightgbm_pipeline() -> Pipeline:
    preprocessador = create_preprocessor()

    model = LGBMClassifier(
        n_estimators=100,  # n° de árvores 
        learning_rate=0.1, # taxa de aprendizaado
        max_depth=3,       # profundidade
        random_state=42    # semente para reproduzibilidade
    )

    return Pipeline(
        steps=[("preprocessor", preprocessador), 
               ("model", model)]
    )
