import pandas as pd
from pathlib import Path
from loguru import logger


def load_data(
    orders_path: Path,
    items_path: Path,
    customers_path: Path
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:

    orders = pd.read_csv(
        orders_path,
        parse_dates=[
            "order_purchase_timestamp",
            "order_approved_at",
            "order_delivered_customer_date",
            "order_delivered_carrier_date",
            "order_estimated_delivery_date"
        ]
    )

    items = pd.read_csv(items_path)

    customers = pd.read_csv(customers_path)

    return orders, items, customers


def save_dataset(
    dataset: pd.DataFrame,
    output_path: Path
) -> None:

    dataset.to_csv(output_path, index=False)

    logger.success(
        f"Dataset saved at {output_path}"
    )


def create_target(
    orders: pd.DataFrame
) -> pd.DataFrame:

    delivered_orders = orders.loc[
        orders["order_status"].eq("delivered")
        & orders["order_delivered_customer_date"].notna()
        & orders["order_estimated_delivery_date"].notna()
        & orders["order_approved_at"].notna()
    ].copy()

    delivered_orders["is_late"] = (
        delivered_orders["order_delivered_customer_date"]
        > delivered_orders["order_estimated_delivery_date"]
    ).astype("int8")

    logger.info(
        f"Pedidos originais: {len(orders):,}"
    )

    logger.info(
        f"Pedidos no recorte histórico: {len(delivered_orders):,}"
    )

    logger.info(
        f"Distribuição da variável alvo:\n"
        f"{delivered_orders['is_late'].value_counts(dropna=False).to_string()}"
    )

    return delivered_orders


def aggregate_items(
    items: pd.DataFrame
) -> pd.DataFrame:

    items_agg = (
        items
        .groupby(
            "order_id",
            as_index=False
        )
        .agg(
            item_count=("order_item_id", "count"),
            seller_count=("seller_id", "nunique"),
            total_price=("price", "sum"),
            total_freight=("freight_value", "sum")
        )
    )

    assert items_agg["order_id"].is_unique

    return items_agg


def create_dataset(
    orders: pd.DataFrame,
    items: pd.DataFrame,
    customers: pd.DataFrame
) -> pd.DataFrame:

    orders = create_target(orders)

    items_agg = aggregate_items(items)

    data = orders.merge(
        items_agg,
        on="order_id",
        how="left",
        validate="one_to_one"
    )

    data = data.merge(
        customers[
            [
                "customer_id",
                "customer_city",
                "customer_state"
            ]
        ],
        on="customer_id",
        how="left",
        validate="many_to_one"
    )

    return data