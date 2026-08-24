import pandas as pd
from sklearn.model_selection import train_test_split

FEATURES = [
    "purchase_hour",
    "purchase_weekday",
    "purchase_month",
    "promised_days",
    "item_count",
    "seller_count",
    "total_price",
    "total_freight",
    "customer_state",

]

TARGET = "is_late"

def split_data(data: pd.DataFrame) -> tuple:
    """
    Dividir o dataset em treino e teste.
    """
    X = data[FEATURES]
    y = data[TARGET]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.20,
        stratify=y,
        random_state=42
    )

    return X_train, X_test, y_train, y_test   