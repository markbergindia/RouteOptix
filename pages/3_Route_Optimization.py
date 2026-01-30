import streamlit as st
import pandas as pd
import numpy as np
import pickle
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="Route Optimization", layout="wide")

if not st.session_state.get('logged_in'):
    st.warning("Please login from the main page.")
    st.stop()

st.title("🚀 Smart Route Optimization")

# Load Models
@st.cache_resource
def load_reg_models():
    try:
        with open('models/saved/model_cost.pkl', 'rb') as f:
            m_cost = pickle.load(f)
        with open('models/saved/model_delay.pkl', 'rb') as f:
            m_delay = pickle.load(f)
        return m_cost, m_delay
    except:
        return None, None

m_cost, m_delay = load_reg_models()

if m_cost is None:
    st.error("Models not found/trained.")
    st.stop()

# CO2 Emission Factors (g CO2 per ton-km)
CO2_FACTORS = {
    'Air': 500,
    'Road': 62,
    'Rail': 22,
    'Sea': 10
}

# Inputs
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("Shipment Details")
    origin = st.selectbox("Origin", ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Miami', 'Seattle', 'Boston', 'Atlanta'])
    dest = st.selectbox("Destination", ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Miami', 'Seattle', 'Boston', 'Atlanta'], index=1)
    weight = st.number_input("Weight (kg)", 10, 10000, 500)
    
    # Mock distance logic (in real app, use Geocoding API)
    mock_dist = (len(origin) + len(dest)) * 100 + abs(ord(origin[0]) - ord(dest[0])) * 50
    st.caption(f"Estimated Distance: {mock_dist} km")
    
    # ⚙️ Constraints Filters
    st.markdown("### ⚠️ Operational Constraints")
    max_budget = st.number_input("Max Budget ($)", value=10000, step=100)
    max_time = st.number_input("Max Delivery Time (Hours)", value=100, step=5)
    
    if st.button("Optimize Route"):
        if origin == dest:
            st.error("Origin and Destination cannot be the same.")
        else:
            # Predict for all modes
            modes = ['Air', 'Road', 'Rail', 'Sea']
            results = []
            
            for mode in modes:
                # Prepare input DF
                input_data = pd.DataFrame([{
                    'Mode': mode,
                    'Distance': mock_dist,
                    'Weight': weight
                }])
                
                pred_cost = m_cost.predict(input_data)[0]
                pred_delay = m_delay.predict(input_data)[0]
                total_time = (mock_dist / {'Air': 800, 'Road': 60, 'Rail': 80, 'Sea': 30}[mode]) + pred_delay
                
                # CO2 Calc: (Distance km * Weight tons * Factor) / 1000 to get kg
                weight_tons = weight / 1000
                co2_kg = (mock_dist * weight_tons * CO2_FACTORS[mode]) / 1000
                
                # Check Constraints
                is_valid = (pred_cost <= max_budget) and (total_time <= max_time)
                
                results.append({
                    'Mode': mode,
                    'Cost ($)': round(pred_cost, 2),
                    'Total Time (hrs)': round(total_time, 2),
                    'Delay Risk (hrs)': round(pred_delay, 2),
                    'CO2 Impact (kg)': round(co2_kg, 2),
                    'Valid': is_valid
                })
            
            df_res = pd.DataFrame(results)
            
            # Filter Valid Options for Best Selection
            valid_opts = df_res[df_res['Valid'] == True]
            
            if not valid_opts.empty:
                best_cost = valid_opts.loc[valid_opts['Cost ($)'].idxmin()]
                best_time = valid_opts.loc[valid_opts['Total Time (hrs)'].idxmin()]
                best_eco = valid_opts.loc[valid_opts['CO2 Impact (kg)'].idxmin()]
            else:
                # Fallback to overall best if nothing meets constraints
                best_cost = df_res.loc[df_res['Cost ($)'].idxmin()]
                best_time = df_res.loc[df_res['Total Time (hrs)'].idxmin()]
                best_eco = df_res.loc[df_res['CO2 Impact (kg)'].idxmin()]
                st.warning(f"No options met your constraints! Showing best available:")
            
            st.session_state['opt_results'] = df_res
            st.session_state['best_cost'] = best_cost
            st.session_state['best_time'] = best_time
            st.session_state['best_eco'] = best_eco

with col2:
    st.subheader("Optimization Results")
    if 'opt_results' in st.session_state:
        res = st.session_state['opt_results']
        
        # Cards
        c1, c2, c3 = st.columns(3)
        c1.metric("💰 Cheapest", f"{st.session_state['best_cost']['Mode']}", f"${st.session_state['best_cost']['Cost ($)']}")
        c2.metric("⚡ Fastest", f"{st.session_state['best_time']['Mode']}", f"{st.session_state['best_time']['Total Time (hrs)']} hrs")
        c3.metric("🌿 Eco-Friendly", f"{st.session_state['best_eco']['Mode']}", f"{st.session_state['best_eco']['CO2 Impact (kg)']} kg CO2")
        
        st.dataframe(res.style.highlight_min(axis=0, subset=['Cost ($)', 'Total Time (hrs)', 'CO2 Impact (kg)'], color='rgba(0, 255, 0, 0.2)'))
        
        st.info(f"Recommendation: **{st.session_state['best_eco']['Mode']}** is the greenest choice. "
                f"**{st.session_state['best_cost']['Mode']}** is the cheapest.")
        
        # Map Visualization (Mocked straight line)
        coords = {
            'New York': [40.7128, -74.0060], 'Los Angeles': [34.0522, -118.2437],
            'Chicago': [41.8781, -87.6298], 'Houston': [29.7604, -95.3698],
            'Miami': [25.7617, -80.1918], 'Seattle': [47.6062, -122.3321],
            'Boston': [42.3601, -71.0589], 'Atlanta': [33.7490, -84.3880]
        }
        
        m = folium.Map(location=[39.8283, -98.5795], zoom_start=4)
        
        p1 = coords[origin]
        p2 = coords[dest]
        
        folium.Marker(p1, tooltip="Origin", icon=folium.Icon(color="green")).add_to(m)
        folium.Marker(p2, tooltip="Destination", icon=folium.Icon(color="red")).add_to(m)
        folium.PolyLine([p1, p2], color="blue", weight=2.5, opacity=1).add_to(m)
        
        st_folium(m, width=900, height=500)
    else:
        st.info("Enter shipment details and click Optimize.")
