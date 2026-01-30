import streamlit as st
import pandas as pd
import plotly.express as px
import sqlite3

st.set_page_config(page_title="Dashboard", layout="wide")

if not st.session_state.get('logged_in'):
    st.warning("Please login from the main page.")
    st.stop()

st.title("📊 Supply Chain Dashboard")

# Load Data
try:
    conn = sqlite3.connect("supply_chain.db")
    df_demand = pd.read_sql("SELECT * FROM demand_history", conn)
    df_transport = pd.read_sql("SELECT * FROM transport_logs", conn)
    conn.close()
except:
    st.error("Data not found. Please ensure data generation completed.")
    st.stop()

# Layout
col1, col2 = st.columns(2)

with col1:
    st.subheader("Demand Overview")
    st.metric("Total Historical Demand", f"{df_demand['Quantity'].sum():,}")
    
    # Demand by Region
    fig_region = px.bar(df_demand.groupby('Region')['Quantity'].sum().reset_index(), 
                        x='Region', y='Quantity', title="Demand by Region", color='Region')
    st.plotly_chart(fig_region, use_container_width=True)
    
    # Demand by Product
    fig_prod = px.pie(df_demand.groupby('Product')['Quantity'].sum().reset_index(), 
                      values='Quantity', names='Product', title="Product Distribution")
    st.plotly_chart(fig_prod, use_container_width=True)

with col2:
    st.subheader("Logistics Overview")
    st.metric("Total Shipments Logged", f"{len(df_transport):,}")
    
    # Cost by Mode
    avg_cost = df_transport.groupby('Mode')['Cost'].mean().reset_index()
    fig_cost = px.bar(avg_cost, x='Mode', y='Cost', title="Average Shipping Cost by Mode", color='Mode')
    st.plotly_chart(fig_cost, use_container_width=True)
    
    # Delay by Mode
    avg_delay = df_transport.groupby('Mode')['Delay_Hours'].mean().reset_index()
    fig_delay = px.bar(avg_delay, x='Mode', y='Delay_Hours', title="Average Delay (Hours) by Mode", color='Mode')
    st.plotly_chart(fig_delay, use_container_width=True)

st.subheader("Recent Activity")
st.dataframe(df_transport.head(10))
