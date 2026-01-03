🌤️ Serverless Global Weather Data Pipeline
An end-to-end data engineering pipeline that ingests, stores, and visualizes real-time weather data for major global cities (London, New York, Tokyo, Kolkata, Delhi, Cairo). Built entirely on the AWS Free Tier using a serverless architecture.

🔗 Live Dashboard Link (Replace with your actual link)

🏗️ Architecture
The system follows a modern Extract-Load-Transform (ELT) pattern:

Code snippet

graph LR
    A[Open-Meteo API] -->|JSON| B(AWS Lambda)
    B -->|Raw JSON Backup| C[AWS S3 Bucket]
    B -->|Structured Data| D[(AWS RDS PostgreSQL)]
    D -->|SQL Queries| E[Streamlit Dashboard]
    E -->|Analytics| F[User Interface]
Ingestion: An AWS Lambda function triggers (scheduled via EventBridge) to fetch real-time weather data from the Open-Meteo API.

Storage (Data Lake): Raw JSON responses are archived in AWS S3 for audit trails and backup.

Storage (Data Warehouse): Structured data (City, Temp, Timestamp) is parsed and loaded into AWS RDS (PostgreSQL).

Visualization: A Streamlit web app connects to the database to provide an interactive dashboard with filtering and historical trends.

🛠️ Tech Stack
Cloud Provider: AWS (eu-north-1)

Compute: AWS Lambda (Serverless Python functions)

Storage: AWS S3 (Object Storage), AWS RDS (Relational Database)

Database: PostgreSQL

IaC / Deployment: Python (Boto3), Streamlit Cloud

Visualization: Streamlit, Pandas, Seaborn

Version Control: Git & GitHub

🌟 Key Features
Multi-City Tracking: specific handling for 6 global locations including Timezone adjustments.

Dual-Layer Storage: Implements "Data Lake" (S3) and "Data Warehouse" (RDS) best practices.

Resilience: Error handling in Lambda ensures one city failure does not crash the pipeline.

Secure: Database credentials managed via AWS Environment Variables and Streamlit Secrets (no hardcoded keys).

Interactive UI: Dynamic SQL queries allow users to filter data by city in real-time.

🚀 How to Run Locally
Clone the repository:

Bash

git clone https://github.com/VermilionSkye/aws-weather-pipeline.git
cd aws-weather-pipeline
Install dependencies:

Bash

pip install -r requirements.txt
Configure Secrets: Create a .streamlit/secrets.toml file with your database credentials:

Ini, TOML

DB_HOST = "your-rds-endpoint"
DB_USER = "your-username"
DB_PASSWORD = "your-password"
Run the App:

Bash

streamlit run app.py
📈 Future Improvements
[ ] Automated Scheduling: Implement AWS EventBridge for hourly triggers.

[ ] Advanced Analytics: Add comparative analysis (e.g., "Hottest City vs. Coldest City").

[ ] Alerting: Set up SNS notifications for extreme weather conditions.