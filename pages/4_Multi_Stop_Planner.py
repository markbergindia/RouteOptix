import streamlit as st
import folium
from streamlit_folium import st_folium
import pandas as pd
import numpy as np
from scipy.spatial.distance import pdist, squareform

st.set_page_config(page_title="Multi-Stop Planner", layout="wide")

if not st.session_state.get('logged_in'):
    st.warning("Please login from the main page.")
    st.stop()
    
st.title("🚚 Multi-Stop Delivery Planner")
st.markdown("Optimize the sequence of deliveries to minimize total distance (TSP).")

# Fixed Dataset of Locations (Mock Geocoding)
LOCATIONS = {
    'New York': [40.7128, -74.0060],
    'Los Angeles': [34.0522, -118.2437],
    'Chicago': [41.8781, -87.6298],
    'Houston': [29.7604, -95.3698],
    'Miami': [25.7617, -80.1918],
    'Seattle': [47.6062, -122.3321],
    'Boston': [42.3601, -71.0589],
    'Atlanta': [33.7490, -84.3880],
    'Denver': [39.7392, -104.9903],
    'San Francisco': [37.7749, -122.4194]
}

col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("Select Stops")
    selected_cities = st.multiselect("Choose Cities to Visit", list(LOCATIONS.keys()), default=['New York', 'Boston', 'Chicago'])
    
    start_city = st.selectbox("Start/End City", selected_cities) if selected_cities else None
    
    if st.button("Optimize Route"):
        if not start_city or len(selected_cities) < 3:
            st.error("Select at least 3 cities.")
        else:
            # TSP Heuristic (Nearest Neighbor)
            # 1. Build Distance Matrix (Euclidean for simplicity)
            cities = [start_city] + [c for c in selected_cities if c != start_city]
            coords = np.array([LOCATIONS[c] for c in cities])
            
            # Simple Nearest Neighbor Logic
            unvisited = set(range(1, len(cities)))
            current_idx = 0
            path_indices = [0]
            
            while unvisited:
                dists = np.linalg.norm(coords[current_idx] - coords[list(unvisited)], axis=1)
                nearest_local_idx = np.argmin(dists)
                nearest_global_idx = list(unvisited)[nearest_local_idx]
                
                path_indices.append(nearest_global_idx)
                unvisited.remove(nearest_global_idx)
                current_idx = nearest_global_idx
                
            path_indices.append(0) # Return to start
            
            optimized_route = [cities[i] for i in path_indices]
            st.session_state['tsp_route'] = optimized_route

with col2:
    if 'tsp_route' in st.session_state:
        route = st.session_state['tsp_route']
        
        st.subheader("Optimized Delivery Sequence")
        st.markdown(f"**Path**: {' ➔ '.join(route)}")
        
        # Map
        m = folium.Map(location=[39.8283, -98.5795], zoom_start=4)
        
        points = [LOCATIONS[c] for c in route]
        
        folium.PolyLine(points, color="purple", weight=3, opacity=0.8).add_to(m)
        
        for i, city in enumerate(route[:-1]): # Don't double label start
            folium.Marker(
                LOCATIONS[city], 
                tooltip=f"{i+1}. {city}", 
                icon=folium.Icon(color="blue" if i==0 else "purple", icon="truck", prefix="fa")
            ).add_to(m)
            
        st_folium(m, width=900, height=500)
    else:
        st.info("Select stops to generate a route map.")
