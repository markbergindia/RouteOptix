import streamlit as st
import pandas as pd
import numpy as np
import folium
from streamlit_folium import st_folium
import plotly.express as px
import time

st.set_page_config(page_title="Risk & Performance", layout="wide")

if not st.session_state.get('logged_in'):
    st.warning("Please login from the main page.")
    st.stop()

st.title("radar Risk & Performance Intelligence")

# 1. Supplier / Carrier Performance Scoring
st.header("🏆 Carrier Performance Scoring")
# Mock Carrier Data (Since we don't have carrier names in logs, we simulate)
carriers = pd.DataFrame({
    'Carrier': ['FedEx', 'DHL', 'UPS', 'Maersk', 'DB Schenker', 'USPS'],
    'Mode': ['Air', 'Air', 'Road', 'Sea', 'Rail', 'Road'],
    'Deliveries': np.random.randint(100, 500, 6),
    'On_Time_Rate': np.random.uniform(85, 99, 6),
    'Avg_Delay_Hrs': np.random.uniform(2, 24, 6),
    'Cost_Efficiency': np.random.uniform(1, 10, 6) # Score 1-10
})
carriers['Score'] = (carriers['On_Time_Rate'] * 0.6) + (carriers['Cost_Efficiency'] * 4) # Simple weight
carriers = carriers.sort_values('Score', ascending=False)

st.dataframe(carriers.style.background_gradient(subset=['On_Time_Rate', 'Score'], cmap='Greens'))

# 2. Risk Zone Heatmap
st.header("🔥 Risk Zone Heatmap")
st.caption("Visualizing regions with high average delays.")

# Mock Risk Zones
risk_locs = [
    [40.7128, -74.0060, 2.5], # NY - mod delay
    [34.0522, -118.2437, 8.0], # LA - high delay (port)
    [41.8781, -87.6298, 4.0], # Chicago
    [25.7617, -80.1918, 1.2], # Miami
    [29.7604, -95.3698, 5.5]  # Houston
]

m = folium.Map(location=[39.8283, -98.5795], zoom_start=4)
from folium.plugins import HeatMap
HeatMap(risk_locs, radius=25).add_to(m)

st_folium(m, width=900, height=400)

# 3. Shipment Tracking Simulation
st.header("📦 Shipment Tracking Simulation")
col1, col2 = st.columns([1, 2])

with col1:
    track_id = st.text_input("Enter Shipment ID", "TRK-9821203")
    if st.button("Track Status"):
        with st.spinner("Fetching Satellite Data..."):
            time.sleep(1.5)
            st.success("Shipment Found!")
            st.session_state['tracking_active'] = True

with col2:
    if st.session_state.get('tracking_active'):
        # Simulated Status
        stages = ["Order Placed", "Packed", "In Transit", "Out for Delivery", "Delivered"]
        current_stage = 2 # In Transit
        
        st.write(f"**Status for {track_id}:** In Transit 🚚")
        
        # Progress Bar
        st.progress(60)
        
        st.markdown(f"""
        - ✅ **Order Placed**: 2023-10-24 09:00 AM
        - ✅ **Packed**: 2023-10-24 02:30 PM
        - 🔵 **In Transit**: Arrived at Hub (Chicago), Est. Arrival 2 days.
        - ⚪ **Out for Delivery**: Pending
        - ⚪ **Delivered**: Pending
        """)
        
        # Exception Management check
        if np.random.random() > 0.7:
            st.warning("⚠️ Exception Detected: Weather Delay in Route. Corrective Action: Re-routing suggested via Rail.")
        else:
            st.success("✅ No exceptions detected. On track.")
