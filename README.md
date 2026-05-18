# MCI2026 Task 2 - Pipeline Orchestration & Data Visualization

| Nama             | NRP           |
| ---------------- | --------------|
| Shifa Alya Dewi  | 5025241176    |


## Project Overview

Project ini bertujuan untuk membangun data pipeline menggunakan Apache Airflow untuk melakukan proses ETL (Extract, Transform, Load) dari API dataset orders ke database ClickHouse, kemudian divisualisasikan menggunakan Metabase.

Pipeline ini dijalankan menggunakan Docker Compose agar seluruh service dapat berjalan secara terintegrasi.

---

# Technologies Used

* Apache Airflow
* ClickHouse
* Metabase
* Docker & Docker Compose
* Python
* Pandas

---

# Dataset

Dataset yang digunakan:

```text
http://96.9.212.102:8000/orders
```

Dataset berisi informasi orders seperti:

* order_id
* user_id
* eval_set
* order_number
* order_dow
* order_hour_of_day
* days_since_prior_order

---

# Project Architecture

```text
Orders API
    ↓
Apache Airflow
    ↓
Parquet File (Data Lake)
    ↓
ClickHouse Database
    ↓
Metabase Dashboard
```

---

# Docker Services

Project menggunakan beberapa container Docker:

| Service           | Description                  |
| ----------------- | ---------------------------- |
| Airflow Webserver | UI Apache Airflow            |
| Airflow Scheduler | Scheduler DAG                |
| PostgreSQL        | Metadata database Airflow    |
| ClickHouse        | Data warehouse               |
| Metabase          | Data visualization dashboard |

---

# Airflow DAG

Pipeline terdiri dari 2 task utama:

## 1. fetch_orders

Task ini bertugas:

* Mengambil data dari Orders API
* Mengubah data JSON menjadi DataFrame
* Menyimpan data ke format parquet

## 2. process_orders

Task ini bertugas:

* Membaca file parquet
* Membuat database dan tabel di ClickHouse
* Memasukkan data ke ClickHouse

---

# DAG Flow

```text
fetch_orders → process_orders
```

---

# Database Schema

Database:

```sql
CREATE DATABASE IF NOT EXISTS mci_orders;
```

Table:

```sql
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
ORDER BY order_id;
```

---

# Example SQL Queries

## Total Orders

```sql
SELECT COUNT(*) AS total_orders
FROM mci_orders.orders;
```

## Unique Users

```sql
SELECT COUNT(DISTINCT user_id) AS total_users
FROM mci_orders.orders;
```

## Orders by Eval Set

```sql
SELECT
    eval_set,
    COUNT(*) AS total
FROM mci_orders.orders
GROUP BY eval_set;
```

## Orders by Hour

```sql
SELECT
    order_hour_of_day,
    COUNT(*) AS total_orders
FROM mci_orders.orders
GROUP BY order_hour_of_day
ORDER BY order_hour_of_day;
```

## Orders by Day

```sql
SELECT
    CASE
        WHEN order_dow = 0 THEN 'Sunday'
        WHEN order_dow = 1 THEN 'Monday'
        WHEN order_dow = 2 THEN 'Tuesday'
        WHEN order_dow = 3 THEN 'Wednesday'
        WHEN order_dow = 4 THEN 'Thursday'
        WHEN order_dow = 5 THEN 'Friday'
        WHEN order_dow = 6 THEN 'Saturday'
    END AS day_name,
    COUNT(*) AS total_orders
FROM mci_orders.orders
GROUP BY order_dow
ORDER BY order_dow;
```

---

# Metabase Dashboard

Dashboard dibuat menggunakan Metabase dengan berbagai visualisasi seperti:

* KPI Cards
* Bar Chart
* Pie Chart
* Line Chart
* Area Chart

Dashboard digunakan untuk menganalisis:

* Total orders
* Unique users
* Peak ordering hours
* Distribution of order numbers
* Weekend vs weekday orders
* Order frequency by day and hour

---

# Project Result

Project berhasil:

* Menjalankan orchestration menggunakan Apache Airflow
* Menyimpan data ke ClickHouse
* Membuat visualisasi menggunakan Metabase
* Menampilkan dashboard analytics secara interaktif

---

# Documentation Screenshots

## Airflow DAG

<img width="956" height="484" alt="Screenshot 2026-05-18 172003" src="https://github.com/user-attachments/assets/19a1d90d-7c06-4fc9-9c5b-0bacd84c3270" />

## DAG Graph

<img width="960" height="477" alt="Screenshot 2026-05-18 180816" src="https://github.com/user-attachments/assets/9e3f3016-6bdc-454f-bad7-de2ae5c4e832" />

## ClickHouse Query

<img width="753" height="367" alt="image" src="https://github.com/user-attachments/assets/0f194ca8-74a1-45de-a6e8-1f93aa6309be" />

<img width="755" height="371" alt="image" src="https://github.com/user-attachments/assets/b91a4453-6533-45b9-a7d7-a37bdafdd1db" />

## Metabase Dashboard

<img width="339" height="477" alt="Screenshot 2026-05-18 173917" src="https://github.com/user-attachments/assets/3fd415f2-b305-49b2-88cf-1f56b78809dc" />

---

# How to Run

## Clone Repository

```bash
git clone <repository-url>
```

## Run Docker Compose

```bash
docker-compose up --build
```

## Access Services

| Service    | URL                                            |
| ---------- | ---------------------------------------------- |
| Airflow    | [http://localhost:8080](http://localhost:8080) |
| Metabase   | [http://localhost:3000](http://localhost:3000) |
| ClickHouse | localhost:9000                                 |

---


