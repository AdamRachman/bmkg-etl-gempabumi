# BMKG Earthquake ETL Pipeline

## Overview

Project ini merupakan implementasi end-to-end ETL (Extract, Transform, Load) Pipeline menggunakan data gempa bumi real-time milik BMKG (Badan Meteorologi, Klimatologi, dan Geofisika). Pipeline dibangun untuk mensimulasikan workflow Data Engineering modern, dimulai dari proses multi-source data ingestion berbasis XML, transformasi dan normalisasi data, orchestration menggunakan Apache Airflow, hingga penyimpanan data ke PostgreSQL dan Google BigQuery.

Project ini awalnya dibangun menggunakan local environment dengan PostgreSQL sebagai relational database, kemudian dikembangkan menjadi hybrid cloud architecture dengan integrasi Google BigQuery sebagai analytical data warehouse.

Tujuan utama project ini adalah memperkuat pemahaman dan implementasi practical terkait:

* ETL Pipeline Development
* Data Transformation & Normalization
* Workflow Orchestration
* Relational & Analytical Database
* Hybrid Cloud Data Architecture
* Google Cloud Platform Ecosystem
* Data Warehouse Integration

---

# Architecture

```text
BMKG XML API Sources
        ↓
    Extract Layer
        ↓
 Transform & Normalization
        ↓
 ┌─────────────────────┐
 │                     │
 ↓                     ↓
PostgreSQL         BigQuery
(Operational DB)   (Analytical Warehouse)
        ↓
 Apache Airflow Orchestration
```

---

# Data Source

Project ini menggunakan dua endpoint XML milik BMKG:

## 1. gempadirasakan.xml

Berisi data gempa bumi yang dirasakan oleh masyarakat.

Source:
https://data.bmkg.go.id/DataMKG/TEWS/gempadirasakan.xml

## 2. gempaterkini.xml

Berisi data gempa bumi terbaru dengan magnitude ≥ 5.0.

Source:
https://data.bmkg.go.id/DataMKG/TEWS/gempaterkini.xml

---

# Key Features

## Multi-Source Data Ingestion

Pipeline melakukan ingestion data dari beberapa endpoint XML BMKG dan menggabungkannya ke dalam satu workflow ETL.

## Schema Normalization

Struktur data dari beberapa source dinormalisasi ke dalam satu schema agar lebih konsisten dan meminimalisir NULL value yang tidak diperlukan.

## Deduplication Logic

Pipeline memiliki mekanisme deduplication untuk mencegah data duplikat masuk ke database.

Validasi dilakukan menggunakan kombinasi:

* datetime_utc
* koordinat

Pendekatan ini membuat pipeline memiliki konsep incremental loading.

## Hybrid Database Architecture

Project ini menggunakan dua jenis database untuk mensimulasikan arsitektur Data Engineering modern.

### PostgreSQL

Digunakan sebagai:

* Relational Database lokal
* Operational / transactional storage
* Environment development ETL

### BigQuery

Digunakan sebagai:

* Cloud analytical data warehouse
* Simulasi analytical workload
* Integrasi ecosystem GCP

## Apache Airflow Orchestration

Apache Airflow digunakan untuk automation, orchestration, scheduling, dan monitoring ETL Pipeline menggunakan konsep DAG.

## Google Cloud Platform Integration

Project telah terintegrasi dengan beberapa layanan GCP seperti:

* BigQuery
* IAM Service Account
* Cloud-based analytical workflow

---

# Tech Stack

| Category               | Technologies                |
| ---------------------- | --------------------------- |
| Programming Language   | Python                      |
| Workflow Orchestration | Apache Airflow              |
| Relational Database    | PostgreSQL                  |
| Cloud Data Warehouse   | Google BigQuery             |
| Data Processing        | Pandas                      |
| XML Parsing            | ElementTree                 |
| Cloud Platform         | Google Cloud Platform (GCP) |
| Authentication         | IAM Service Account         |
| ETL Utilities          | SQLAlchemy, psycopg2        |

---

# Database Schema

| Column Name  | Description            |
| ------------ | ---------------------- |
| tanggal      | Tanggal gempa          |
| jam          | Waktu gempa            |
| datetime_utc | Timestamp UTC          |
| koordinat    | Titik koordinat        |
| lintang      | Representasi latitude  |
| bujur        | Representasi longitude |
| magnitude    | Magnitude gempa        |
| kedalaman_km | Kedalaman gempa        |
| wilayah      | Lokasi / wilayah gempa |
| skala_gempa  | Kategori skala gempa   |
| source_data  | Identifier source data |
| created_at   | Timestamp insert ETL   |

---

# Transformation Process

Layer transformasi melakukan beberapa proses penting:

## Standardization

Perbedaan struktur XML dari masing-masing source dinormalisasi menjadi satu format schema.

## Data Type Conversion

* Konversi datetime
* Konversi numeric magnitude
* Konversi numeric kedalaman

## Data Cleaning

* Pembersihan format depth
* Handling invalid values
* Duplicate removal

## Derived Columns

### skala_gempa

Dibuat berdasarkan nilai magnitude.

| Magnitude | Category |
| --------- | -------- |
| < 4       | Lemah    |
| 4 - <5    | Ringan   |
| 5 - <6    | Sedang   |
| ≥ 6       | Kuat     |

### source_data

Digunakan untuk mengidentifikasi source asal data BMKG.

---

# Airflow Orchestration

Workflow ETL diorkestrasi menggunakan Apache Airflow.

## Workflow Stages

1. Extract data dari BMKG XML API
2. Transformasi & normalisasi data
3. Validasi dan deduplication
4. Load ke PostgreSQL atau BigQuery
5. Validasi final row count

## Scheduling

DAG dapat dijalankan secara otomatis menggunakan Airflow Scheduler.

---

# BigQuery Integration

Project ini dikembangkan menjadi hybrid cloud implementation dengan integrasi Google BigQuery.

## Mengapa BigQuery?

BigQuery digunakan untuk mensimulasikan cloud-native analytical workflow karena memiliki:

* Serverless architecture
* High scalability
* Fast analytical query processing
* Native integration dengan ecosystem GCP

## Authentication

Authentication dilakukan menggunakan IAM Service Account milik GCP.

---

# Project Structure

```text
bmkg-etl-gempabumi/
│
├── dags/
│   ├── bmkg_postgres_etl_dag.py
│   └── bmkg_bigquery_etl_dag.py
│
├── scripts/
│   ├── extract.py
│   ├── transform.py
│   ├── load_postgres.py
│   ├── load_bigquery.py
│   ├── main_postgres.py
│   └── main_bigquery.py
│
├── screenshots/
│
├── README.md
├── requirements.txt
└── .gitignore
```

---

# Future Improvements

Beberapa pengembangan yang direncanakan:

* Migrasi orchestration ke Cloud Composer
* Docker containerization
* Data quality validation layer
* Dashboard & reporting integration
* Cloud Storage raw layer
* CI/CD automation

---

# Learning Outcomes

Melalui project ini, beberapa konsep Data Engineering berhasil dipelajari dan diimplementasikan:

* ETL Pipeline Development
* Workflow Orchestration
* Data Normalization
* Incremental Loading
* Deduplication Strategy
* Relational vs Analytical Database
* Hybrid Cloud Architecture
* BigQuery Integration
* IAM Authentication
* Airflow Scheduling

---

# Screenshots

![Architecture](./screenshots/architecture.png)
![Airflow DAG UI](./screenshots/airflow_dag.png)
![BigQuery Table Preview](./screenshots/bmkg-table-preview.png)
![BigQuery Data Results](./screenshots/bigquery-data-preview.png)
![PostgreSQL Table Contents](./screenshots/postgres-table-preview.png)![PostgreSQL Data Contents](./screenshots/postgres-table-preview.png)
![ETL Logs](./screenshots/etl_logs.png)

---

# Author

Muhammad Adam Rachman

Information Systems Graduate dengan minat kuat di bidang Data Engineering, ETL Pipeline Development, SQL, Python, Cloud Data Architecture, dan Workflow Orchestration.

LinkedIn:
http://www.linkedin.com/in/adamrchmn
