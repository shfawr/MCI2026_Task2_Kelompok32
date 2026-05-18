import pandas as pd
import requests

url = "http://96.9.212.102:8000/orders"

response = requests.get(url)

data = response.json()

df = pd.DataFrame(data)

print(df.head())

orders_df = pd.json_normalize(df['orders'])

print(orders_df.head())

orders_df.to_parquet(
    '/opt/airflow/data_lake/orders.parquet',
    index=False
)

print("Orders data saved")