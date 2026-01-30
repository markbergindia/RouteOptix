import streamlit as st
import pandas as pd
import numpy as np
import folium
from streamlit_folium import st_folium
import random

st.set_page_config(page_title="Smart Consolidation", layout="wide")

if not st.session_state.get('logged_in'):
    st.warning("Please login from the main page.")
    st.stop()

st.title("📦 Smart Logistics Optimization")
st.markdown("Use AI algorithms for **Order Consolidation** and **Load Capacity Planning**.")

tab1, tab2 = st.tabs(["Smart Order Consolidation", "Load Capacity Optimizer"])

# Mock Order Data
@st.cache_data
def get_pending_orders():
    orders = []
    locations = {
        'New York': [40.7128, -74.0060],
        'Newark': [40.7357, -74.1724], # Near NY
        'Jersey City': [40.7178, -74.0431], # Near NY
        'Boston': [42.3601, -71.0589],
        'Cambridge': [42.3736, -71.1097], # Near Boston
        'Philadelphia': [39.9526, -75.1652]
    }
    
    for i in range(10):
        loc = random.choice(list(locations.keys()))
        orders.append({
            'Order ID': f"ORD-{1000+i}",
            'Location': loc,
            'Coords': locations[loc],
            'Weight (kg)': random.randint(50, 500),
            'Volume (m3)': random.uniform(0.5, 3.0),
            'Status': 'Pending'
        })
    return pd.DataFrame(orders)

df_orders = get_pending_orders()

with tab1:
    st.header("🔗 Order Consolidation")
    st.caption("Automatically group nearby orders to reduce shipment count.")
    
    st.subheader("Pending Orders")
    st.dataframe(df_orders, use_container_width=True)
    
    threshold = st.slider("Consolidation Radius (km)", 10, 200, 50)
    
    if st.button("Run Consolidation Algorithm"):
        st.spinner("Clustering orders...")
        
        # We'll just group by "Hub" manually for demo
        # NY Area
        ny_cluster = df_orders[df_orders['Location'].isin(['New York', 'Newark', 'Jersey City'])]
        # Boston Area
        bos_cluster = df_orders[df_orders['Location'].isin(['Boston', 'Cambridge'])]
        # Others
        others = df_orders[~df_orders['Location'].isin(['New York', 'Newark', 'Jersey City', 'Boston', 'Cambridge'])]
        
        # Save to Session State
        st.session_state['consolidation_results'] = {
            'ny': ny_cluster,
            'bos': bos_cluster,
            'others': others
        }
    
    # Render if results exist
    if 'consolidation_results' in st.session_state:
        res = st.session_state['consolidation_results']
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.success(f"✅ Consolidated {len(res['ny'])} orders into **Shipment #1 (NY Hub)**")
            st.write(res['ny'][['Order ID', 'Location', 'Weight (kg)']])
            
            st.success(f"✅ Consolidated {len(res['bos'])} orders into **Shipment #2 (Boston Hub)**")
            st.write(res['bos'][['Order ID', 'Location', 'Weight (kg)']])
            
        with col2:
            st.info(f"ℹ️ Remaining {len(res['others'])} orders require individual shipping.")
            
            # Map
            m = folium.Map(location=[41.0, -73.0], zoom_start=6)
            
            # Draw Clusters
            for _, row in res['ny'].iterrows():
                folium.Marker(row['Coords'], icon=folium.Icon(color='green', icon='box', prefix='fa')).add_to(m)
            
            for _, row in res['bos'].iterrows():
                folium.Marker(row['Coords'], icon=folium.Icon(color='blue', icon='box', prefix='fa')).add_to(m)
                
            st_folium(m, width=500, height=400)

with tab2:
    st.header("🚛 Load Capacity Optimization")
    st.caption("Optimize vehicle filling rate.")
    
    col_a, col_b = st.columns(2)
    
    with col_a:
        vehicle_type = st.selectbox("Vehicle Type", ["Van (1000kg)", "Truck (5000kg)", "Container (20000kg)"])
        capacity_map = {"Van (1000kg)": 1000, "Truck (5000kg)": 5000, "Container (20000kg)": 20000}
        max_cap = capacity_map[vehicle_type]
        
        st.info(f"Max Capacity: **{max_cap} kg**")
        
        shipment_weight = st.number_input("Total Shipment Weight (kg)", 0, 30000, 4200)
    
    with col_b:
        utilization = (shipment_weight / max_cap) * 100
        
        st.metric("Load Utilization", f"{utilization:.1f}%")
        st.progress(min(utilization/100, 1.0))
        
        if utilization > 100:
            st.error(f"⚠️ Overload! Exceeds capacity by {shipment_weight - max_cap} kg.")
            st.warning("Recommendation: Split into 2 vehicles.")
        elif utilization < 50:
            st.warning("⚠️ Underutilized. Consider consolidating more orders.")
        else:
            st.success("✅ Optimal Load.")
