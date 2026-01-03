import streamlit as st
import psycopg2
import pandas as pd

# 1. Title 
st.title("🌤️ London Weather Data Pipeline")
st.write("This app connects directly to an **AWS RDS (PostgreSQL)** database to visualize hourly weather data collected by AWS Lambda.")

# 2. Connect to Database
@st.cache_data(ttl=600) # Cache data for 10 mins. don't spam the DB!!!
def get_data():
    conn = psycopg2.connect(
        host=st.secrets["postgres"]["host"],
        database=st.secrets["postgres"]["dbname"],
        user=st.secrets["postgres"]["user"],
        password=st.secrets["postgres"]["password"]
    )
    query = "SELECT recorded_at, temperature, city FROM raw_data.weather_logs ORDER BY recorded_at DESC"
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# 3. Load Data
try:
    with st.spinner('Fetching data from AWS...'):
        df = get_data()
    
    # 4. Show "KPI" Metrics
    latest_temp = df.iloc[0]['temperature']
    latest_time = df.iloc[0]['recorded_at']
    
    col1, col2 = st.columns(2)
    col1.metric("Latest Temperature", f"{latest_temp} °C")
    col2.metric("Last Updated", str(latest_time))

    # 5. The Graph
    st.subheader("Temperature Trend")
    st.line_chart(df.set_index('recorded_at')['temperature'])

    # 6. Show Raw Data 
    if st.checkbox('Show Raw Data'):
        st.dataframe(df)

except Exception as e:
    st.error(f"Error connecting to database: {e}") #tehee hope not