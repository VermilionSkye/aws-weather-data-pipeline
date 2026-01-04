import streamlit as st
import pandas as pd
import psycopg2
import os
import seaborn as sns
import matplotlib.pyplot as plt

# --- 1. SETUP PAGE CONFIGURATION ---
st.set_page_config(page_title="Global Weather Dashboard", page_icon="🌤️", layout="wide")

# --- 2. CONNECT TO DATABASE ---
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

# --- 3. DATA FETCHING FUNCTIONS ---
def get_city_data(city_name):
    conn = get_db_connection()
    if conn:
        query = """
            SELECT recorded_at, temperature, city
            FROM raw_data.weather_logs
            WHERE city = %s
            ORDER BY recorded_at DESC
            LIMIT 50
        """
        df = pd.read_sql(query, conn, params=(city_name,))
        return df
    return pd.DataFrame()

def get_comparison_data():
    conn = get_db_connection()
    if conn:
        # Fetch last 100 records for ALL cities to compare
        query = """
            SELECT recorded_at, temperature, city
            FROM raw_data.weather_logs
            ORDER BY recorded_at DESC
            LIMIT 200
        """
        df = pd.read_sql(query, conn)
        return df
    return pd.DataFrame()

# --- 4. SIDEBAR ---
st.sidebar.header("🌍 Settings")
if st.sidebar.button("Refresh Data"):
    st.cache_data.clear()
    st.rerun()

# --- 5. MAIN DASHBOARD ---
st.title("🌤️ Global Weather Intelligence")

# Create Tabs
tab1, tab2 = st.tabs(["🏙️ City Focus", "📈 Global Comparison"])

# === TAB 1: INDIVIDUAL CITY ANALYSIS ===
with tab1:
    selected_city = st.selectbox("Select City", ["London", "New York", "Tokyo", "Kolkata", "New Delhi", "Cairo"])
    
    df_city = get_city_data(selected_city)
    
    if not df_city.empty:
        # Metrics
        latest = df_city.iloc[0]
        col1, col2, col3 = st.columns(3)
        col1.metric("Current Temperature", f"{latest['temperature']} °C")
        col2.metric("Last Updated", str(latest['recorded_at'].time())[:5])
        col3.metric("Datapoints Logged", len(df_city))
        
        # Chart
        st.subheader(f"Temperature Trend: {selected_city}")
        st.line_chart(df_city.set_index('recorded_at')['temperature'])
    else:
        st.info("Waiting for data...")

# === TAB 2: MULTI-CITY COMPARISON ===
with tab2:
    st.subheader("Compare Cities")
    df_all = get_comparison_data()
    
    if not df_all.empty:
        # Pivot the data for the chart: Index=Time, Columns=City, Values=Temp
        # We handle duplicates by averaging just in case timestamps align perfectly
        chart_data = df_all.pivot_table(index='recorded_at', columns='city', values='temperature', aggfunc='mean')
        
        # Render the multi-line chart
        st.line_chart(chart_data)
        
        st.caption("Showing real-time data comparison across all monitored locations.")
    else:
        st.warning("Not enough global data yet.")

# --- 6. FOOTER ---
st.markdown("---")
st.caption("Data Engineering Pipeline | AWS Lambda • RDS • Streamlit")