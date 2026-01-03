# Serverless Global Weather Data Pipeline

![Status](https://img.shields.io/badge/Status-Live-success) ![AWS](https://img.shields.io/badge/AWS-Lambda%20%7C%20S3%20%7C%20RDS-orange) ![Python](https://img.shields.io/badge/Python-3.12-blue) ![Streamlit](https://img.shields.io/badge/Frontend-Streamlit-red)

An end-to-end data engineering pipeline that ingests, stores, and visualizes real-time weather data for major global cities (London, New York, Tokyo, Kolkata, Delhi, Cairo). Built entirely on the AWS Free Tier using a serverless architecture.

**🔗 [Live Dashboard Link](https://aws-weather-data.streamlit.app/)**

---

## Architecture

The system follows a modern Extract-Load-Transform (ELT) pattern:

1.  **Ingestion:** An **AWS Lambda** function triggers (scheduled via EventBridge) to fetch real-time weather data from the Open-Meteo API.
2.  **Storage (Data Lake):** Raw JSON responses are archived in **AWS S3** for audit trails and backup.
3.  **Storage (Data Warehouse):** Structured data (City, Temp, Timestamp) is parsed and loaded into **AWS RDS (PostgreSQL)**.
4.  **Visualization:** A **Streamlit** web app connects to the database to provide an interactive dashboard with filtering and historical trends.

---

## Tech Stack

* **Cloud Provider:** AWS
* **Compute:** AWS Lambda (Serverless Python functions)
* **Storage:** AWS S3 (Object Storage), AWS RDS (Relational Database)
* **Database:** PostgreSQL
* **IaC / Deployment:** Python (Boto3), Streamlit Cloud
* **Visualization:** Streamlit, Pandas, Seaborn
* **Version Control:** Git & GitHub

---

## Key Features

* **Multi-City Tracking:** Specific handling for 6 global locations including Timezone adjustments.
* **Dual-Layer Storage:** Implements "Data Lake" (S3) and "Data Warehouse" (RDS) best practices.
* **Resilience:** Error handling in Lambda ensures one city failure does not crash the pipeline.
* **Secure:** Database credentials managed via AWS Environment Variables and Streamlit Secrets (no hardcoded keys).
* **Interactive UI:** Dynamic SQL queries allow users to filter data by city in real-time.

---

## 🚀 How to Run Locally

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/VermilionSkye/aws-weather-pipeline.git](https://github.com/VermilionSkye/aws-weather-data-pipeline.git)
    cd aws-weather-pipeline
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Configure Secrets:**
    Create a `.streamlit/secrets.toml` file with your database credentials:
    ```toml
    DB_HOST = "your-rds-endpoint"
    DB_USER = "your-username"
    DB_PASSWORD = "your-password"
    ```

4.  **Run the App:**
    ```bash
    streamlit run app.py
    ```

---

## 📈 Future Improvements

* [ ] **Automated Scheduling:** Implement AWS EventBridge for hourly triggers.
* [ ] **Advanced Analytics:** Add comparative analysis (e.g., "Hottest City vs. Coldest City").
* [ ] **Alerting:** Set up SNS notifications for extreme weather conditions.