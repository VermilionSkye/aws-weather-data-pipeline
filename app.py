import streamlit as st
import pandas as pd
import psycopg2
import os
import seaborn as sns
import matplotlib.pyplot as plt

# --- 1. SETUP PAGE CONFIGURATION ---
st.set_page_config(page_title="Global Weather Dashboard", page_icon="🌤️")

# --- 2. CONNECT TO DATABASE ---
# We use st.cache_resource so we don't reconnect every time you click a button
@st.cache_resource
def get_db_connection():
    try:
        conn = psycopg2.connect(
            host=st.secrets["DB_HOST"],
            database="postgres",
            user=st.secrets["DB_USER"],
            password=st.secrets["DB_PASSWORD"]
        )
        return conn
    except Exception as e:
        st.error(f"Error connecting to database: {e}")
        return None

# --- 3. FETCH DATA (Dynamic Filter) ---
def get_data(city_name):
    conn = get_db_connection()
    if conn:
        # SQL Injection Prevention: We use %s placeholders, never f-strings!
        query = """
            SELECT recorded_at, temperature, city
            FROM raw_data.weather_logs
            WHERE city = %s
            ORDER BY recorded_at DESC
            LIMIT 50
        """
        # We pass the city_name as a tuple parameter
        df = pd.read_sql(query, conn, params=(city_name,))
        return df
    return pd.DataFrame()

# --- 4. SIDEBAR CONTROLS ---
st.sidebar.header("🌍 Configuration")
st.sidebar.write("Select a city to analyze:")

# The Dropdown Menu
selected_city = st.sidebar.selectbox(
    "Choose City",
    ["London", "New York", "Tokyo", "Kolkata", "New Delhi", "Cairo"]
)

# Refresh Button
if st.sidebar.button("Refresh Data"):
    st.cache_data.clear()
    st.rerun()

# --- 5. MAIN DASHBOARD ---
st.title(f"🌤️ {selected_city} Weather Tracker")

# Load data for the SELECTED city only
df = get_data(selected_city)

if not df.empty:
    # A. KPIS (Key Performance Indicators)
    latest_temp = df.iloc[0]['temperature']
    last_update = df.iloc[0]['recorded_at']
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Current Temp", f"{latest_temp} °C")
    col2.metric("Last Updated", str(last_update.time())[:5]) # Shows HH:MM
    col3.metric("Data Points", len(df))

    # B. CHART (Temperature Trend)
    st.subheader("Temperature Trend (Last 50 Readings)")
    
    # We use Streamlit's native line chart which is interactive
    st.line_chart(df.set_index('recorded_at')['temperature'])
    
    # C. RAW DATA (Collapsible)
    with st.expander("See Raw Data"):
        st.dataframe(df)

else:
    st.warning(f"No data found for {selected_city}. Run the Lambda function first!")

# --- 6. FOOTER ---
st.markdown("---")
st.caption("Data Engineering Pipeline | AWS Lambda • RDS • Streamlit")