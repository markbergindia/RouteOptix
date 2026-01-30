import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

def generate_demand_data(num_days=365):
    """Generates synthetic demand data for LSTM training."""
    products = ['Electronics', 'Clothing', 'Home_Decor', 'Perishables', 'Industrial_Parts']
    regions = ['North', 'South', 'East', 'West']
    
    data = []
    start_date = datetime.now() - timedelta(days=num_days)
    
    for day in range(num_days):
        current_date = start_date + timedelta(days=day)
        
        for region in regions:
            for product in products:
                # Base demand with some seasonality and noise
                base_demand = random.randint(50, 200)
                seasonal_factor = 1.0 + 0.3 * np.sin(2 * np.pi * day / 365) # Yearly season
                noise = random.normalvariate(0, 10)
                
                quantity = int(base_demand * seasonal_factor + noise)
                quantity = max(10, quantity) # Ensure non-negative
                
                data.append([current_date.strftime('%Y-%m-%d'), product, region, quantity])
                
    df = pd.DataFrame(data, columns=['Date', 'Product', 'Region', 'Quantity'])
    df.to_csv('demand_history.csv', index=False)
    print("Generated demand_history.csv")
    return df

def generate_transport_logs(num_samples=1000):
    """Generates synthetic transportation logs for Cost/Delay regression."""
    modes = ['Air', 'Road', 'Rail', 'Sea']
    cities = ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Miami', 'Seattle', 'Boston', 'Atlanta']
    
    data = []
    
    for _ in range(num_samples):
        origin = random.choice(cities)
        dest = random.choice([c for c in cities if c != origin])
        mode = random.choice(modes)
        
        # Approximate distance (just randomizing for synthetic purpose, normally would use geocoding)
        distance = random.randint(200, 3000) 
        weight = random.randint(10, 5000) # kg
        
        # Calculate Logic (Base + Variances)
        if mode == 'Air':
            cost_per_km = 1.5
            speed_kmh = 800
            delay_factor = 0.1
        elif mode == 'Road':
            cost_per_km = 0.5
            speed_kmh = 60
            delay_factor = 0.3 # Traffic
        elif mode == 'Rail':
            cost_per_km = 0.3
            speed_kmh = 80
            delay_factor = 0.2
        elif mode == 'Sea':
            cost_per_km = 0.1
            speed_kmh = 30
            delay_factor = 0.4 # Port congestion
            
        base_cost = (distance * cost_per_km) + (weight * 0.1)
        cost = base_cost * random.uniform(0.9, 1.2) # Variance
        
        base_time_hours = distance / speed_kmh
        delay_hours = base_time_hours * delay_factor * random.random()
        
        data.append([origin, dest, mode, distance, weight, round(cost, 2), round(delay_hours, 2)])
        
    df = pd.DataFrame(data, columns=['Origin', 'Destination', 'Mode', 'Distance', 'Weight', 'Cost', 'Delay_Hours'])
    df.to_csv('transport_logs.csv', index=False)
    print("Generated transport_logs.csv")
    return df

if __name__ == "__main__":
    generate_demand_data()
    generate_transport_logs()
