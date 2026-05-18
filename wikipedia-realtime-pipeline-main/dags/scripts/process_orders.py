import pandas as pd
from clickhouse_driver import Client

# read parquet
orders_df = pd.read_parquet(
    '/opt/airflow/data_lake/orders.parquet'
)

print(orders_df.head())

# connect clickhouse
client = Client(
    host='clickhouse-server',
    port=9000,
    user='admin',
    password='rahasia'
)

# create database
client.execute("""
CREATE DATABASE IF NOT EXISTS mci_orders
""")

# create table
client.execute("""
CREATE TABLE IF NOT EXISTS mci_orders.orders (
    order_id UInt32,
    user_id UInt32,
    eval_set String,
    order_number UInt32,
    order_dow UInt32,
    order_hour_of_day UInt32,
    days_since_prior_order Float64
)
ENGINE = MergeTree()
ORDER BY order_id
""")

# select columns
insert_df = orders_df[
    [
        'order_id',
        'user_id',
        'eval_set',
        'order_number',
        'order_dow',
        'order_hour_of_day',
        'days_since_prior_order'
    ]
]

# insert
data = [tuple(row) for row in insert_df.to_numpy()]

client.execute(
    'INSERT INTO mci_orders.orders VALUES',
    data
)

print("Data loaded successfully")