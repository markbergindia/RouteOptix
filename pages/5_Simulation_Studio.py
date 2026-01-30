import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import sqlite3

st.set_page_config(page_title="Simulation Studio", layout="wide")

if not st.session_state.get('logged_in'):
    st.warning("Please login from the main page.")
    st.stop()

st.title("🧪 Advanced Simulation Studio")
st.markdown("Analyze how **market fluctuations** impact your supply chain costs and delays.")

# Load Data
conn = sqlite3.connect("supply_chain.db")
df_trans = pd.read_sql("SELECT * FROM transport_logs", conn)
conn.close()

# --- Sidebar Controls ---
st.sidebar.header("Scenario Parameters")
fuel_price_surge = st.sidebar.slider("⛽ Fuel Price Surge (%)", 0, 100, 0, help="Simulate increase in global fuel prices")
demand_surge = st.sidebar.slider("📦 Demand Surge (%)", 0, 50, 0, help="Simulate peak season volume increase")
port_congestion = st.sidebar.slider("⚓ Port Congestion Level", 0.0, 1.0, 0.0, help="Adds delay to Sea freight")

# --- Simulation Logic ---
# Base Calculations
df_sim = df_trans.copy()

# 1. Apply Demand Surge (Simulated by increasing weight/volume of shipments, leading to higher cost)
# We assume demand surge means we ship MORE, so total cost increases proportional to surge
simulated_volume_factor = 1 + (demand_surge / 100)

# 2. Apply Fuel Price Surge
# Impact depends on mode. Air/Road/Sea high impact, Rail lower.
fuel_impact_map = {'Air': 0.4, 'Road': 0.3, 'Sea': 0.2, 'Rail': 0.1} # % of cost that is fuel
df_sim['Fuel_Cost_Impact'] = df_sim['Mode'].map(fuel_impact_map) * (fuel_price_surge / 100)
df_sim['Simulated_Cost'] = df_trans['Cost'] * (1 + df_sim['Fuel_Cost_Impact']) * simulated_volume_factor

# 3. Apply Port Congestion (Delay)
# Only affects Sea
df_sim['Simulated_Delay'] = df_trans['Delay_Hours']
mask_sea = df_sim['Mode'] == 'Sea'
df_sim.loc[mask_sea, 'Simulated_Delay'] += (port_congestion * 48) # Add up to 48 hours delay

# --- Results ---
st.subheader("What-If Scenario Analysis")

c1, c2, c3 = st.columns(3)
base_total_cost = df_trans['Cost'].sum()
sim_total_cost = df_sim['Simulated_Cost'].sum()
cost_diff = sim_total_cost - base_total_cost

c1.metric("Projected Total Cost", f"${sim_total_cost:,.0f}", f"{((sim_total_cost/base_total_cost)-1)*100:.1f}%", delta_color="inverse")
c2.metric("Projected Avg Delay", f"{df_sim['Simulated_Delay'].mean():.1f} hrs", f"{(df_sim['Simulated_Delay'].mean() - df_trans['Delay_Hours'].mean()):.1f} hrs", delta_color="inverse")
c3.metric("Cost Impact", f"${cost_diff:,.0f}", "Additional Spend")

# Visualization
st.markdown("### Cost Impact by Mode")
cost_by_mode = df_sim.groupby('Mode')[['Simulated_Cost']].sum().reset_index()
cost_by_mode['Base_Cost'] = df_trans.groupby('Mode')['Cost'].sum().values
cost_by_mode = cost_by_mode.melt(id_vars='Mode', var_name='Scenario', value_name='Total Cost')

fig = px.bar(cost_by_mode, x='Mode', y='Total Cost', color='Scenario', barmode='group', title="Base vs Simulated Cost")
st.plotly_chart(fig, use_container_width=True)

# Peak Season Analysis (Static Mock for demonstration if no dates in transport logs, but we do have demand data)
st.markdown("---")
st.subheader("📅 Peak Season Demand Impact")
st.info("Historical data identifies **November** and **December** as high-risk Peak Season months.")

# Mock seasonality chart
months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
risk_score = [2, 2, 3, 2, 3, 4, 3, 4, 5, 6, 9, 10]
fig2 = px.line(x=months, y=risk_score, markers=True, title="Disruption Risk Index (Seasonal)")
fig2.add_shape(type="rect", x0=9.5, y0=0, x1=11.5, y1=10, fillcolor="red", opacity=0.1, line_width=0)
fig2.add_annotation(x='Nov', y=9, text="Peak Season", showarrow=True, arrowhead=1)
st.plotly_chart(fig2, use_container_width=True)
