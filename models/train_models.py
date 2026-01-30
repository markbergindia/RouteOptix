import pandas as pd
import numpy as np
import pickle
import os
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout

# Ensure directories exist
os.makedirs('models/saved', exist_ok=True)

def train_demand_forecasting():
    """Trains an LSTM model on demand_history.csv"""
    print("Training Demand Forecasting Model (LSTM)...")
    if not os.path.exists('demand_history.csv'):
        print("Error: demand_history.csv not found.")
        return

    df = pd.read_csv('demand_history.csv')
    
    # Preprocessing: Aggregate by Date
    df['Date'] = pd.to_datetime(df['Date'])
    daily_demand = df.groupby('Date')['Quantity'].sum().reset_index()
    daily_demand = daily_demand.sort_values('Date')
    
    data = daily_demand['Quantity'].values.reshape(-1, 1)
    
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(data)
    
    # Create sequences
    look_back = 30
    X, y = [], []
    for i in range(look_back, len(scaled_data)):
        X.append(scaled_data[i-look_back:i, 0])
        y.append(scaled_data[i, 0])
        
    X, y = np.array(X), np.array(y)
    X = np.reshape(X, (X.shape[0], X.shape[1], 1))
    
    # Build LSTM
    model = Sequential([
        LSTM(50, return_sequences=True, input_shape=(X.shape[1], 1)),
        Dropout(0.2),
        LSTM(50),
        Dropout(0.2),
        Dense(1)
    ])
    
    model.compile(optimizer='adam', loss='mean_squared_error')
    model.fit(X, y, epochs=10, batch_size=32, verbose=1)
    
    # Save Model
    model.save('models/saved/lstm_demand.h5')
    with open('models/saved/scaler_demand.pkl', 'wb') as f:
        pickle.dump(scaler, f)
        
    print("LSTM Model Saved.")

def train_logistics_regression():
    """Trains Regression models for Cost and Delay prediction."""
    print("Training Logistics Regression Models...")
    if not os.path.exists('transport_logs.csv'):
        print("Error: transport_logs.csv not found.")
        return

    df = pd.read_csv('transport_logs.csv')
    
    # Features and Targets
    X = df[['Mode', 'Distance', 'Weight']]
    y_cost = df['Cost']
    y_delay = df['Delay_Hours']
    
    # Pipeline for preprocessing
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', MinMaxScaler(), ['Distance', 'Weight']),
            ('cat', OneHotEncoder(handle_unknown='ignore'), ['Mode'])
        ])
    
    # Train Cost Model
    model_cost = Pipeline(steps=[('preprocessor', preprocessor),
                                 ('regressor', RandomForestRegressor(n_estimators=100))])
    model_cost.fit(X, y_cost)
    
    # Train Delay Model
    model_delay = Pipeline(steps=[('preprocessor', preprocessor),
                                  ('regressor', RandomForestRegressor(n_estimators=100))])
    model_delay.fit(X, y_delay)
    
    # Save Models
    with open('models/saved/model_cost.pkl', 'wb') as f:
        pickle.dump(model_cost, f)
        
    with open('models/saved/model_delay.pkl', 'wb') as f:
        pickle.dump(model_delay, f)
        
    print("Regression Models Saved.")

if __name__ == "__main__":
    train_demand_forecasting()
    train_logistics_regression()
