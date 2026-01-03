# 🌤️ End-to-End AWS Weather Data Pipeline

A full-stack data engineering pipeline that ingests, stores, transforms, and visualizes real-time weather data for London using the AWS Cloud ecosystem.

## 🏗️ Architecture
**Source** (Open-Meteo API) ➡️ **Ingestion** (AWS Lambda + EventBridge) ➡️ **Storage** (AWS RDS PostgreSQL) ➡️ **Transformation** (dbt) ➡️ **Visualization** (Streamlit & Grafana)

## 🛠️ Tech Stack
* **Cloud:** AWS Lambda, Amazon EventBridge, Amazon RDS (PostgreSQL)
* **Infrastructure as Code:** Python (Boto3)
* **Transformation:** dbt (Data Build Tool)
* **Visualization:** Streamlit (Python), Grafana
* **Language:** Python 3.10

## 🚀 Key Features
* **Automated Ingestion:** A serverless Lambda function triggers hourly via EventBridge to fetch live weather data.
* **Data Warehousing:** Raw data is stored in a normalized PostgreSQL schema (`raw_data`).
* **Analytics Engineering:** dbt models transform raw logs into daily aggregations (Avg/Min/Max temperature) in an `analytics` schema.
* **Interactive Dashboard:** A Streamlit app connects directly to the DB to visualize trends and KPIs.

## 📂 Project Structure
```text
├── app.py                  # Streamlit frontend application
├── weather_transform/      # dbt project for data transformation
│   ├── models/             # SQL models for analytics
│   └── dbt_project.yml     # dbt configuration
└── logs/                   # Local logs (ignored in prod)