# RouteOptix: Intelligent Multimodal Supply Chain Optimization 🚛

RouteOptix is an advanced AI-powered platform designed to optimize supply chain logistics. It leverages **Machine Learning (ML)** and **Deep Learning (DL)** to predict demand, estimate transportation costs, and optimize routing decisions.

## 🌟 Key Features
- **Demand Forecasting**: Uses LSTM (Deep Learning) to predict future product demand.
- **Route Optimization**: ML-based prediction of Cost & Delay for multiple transport modes (Air, Road, Rail, Sea).
- **Simulation Studio**: "What-If" analysis for fuel price surges and demand spikes.
- **Risk Intelligence**: Heatmaps and Carrier Performance Scoring.
- **Sustainability**: Carbon (CO2) emission tracking.
- **Operations**: Smart Order Consolidation and Load Capacity Optimization.
- **AI Assistant**: Built-in Chatbot for decision support.

---

## 🛠️ Installation Guide (VS Code)

Follow these steps to set up and run the project in **Visual Studio Code**.

### 1. Prerequisites
- **Python 3.8+** installed.
- **VS Code** installed (Recommended Extensions: *Python*, *Pylance*).

### 2. Setup Environment
1.  Open the project folder (`RouteOptix`) in VS Code.
2.  Open the **Terminal** (`Ctrl + ` `).
3.  Install the required libraries:
    ```powershell
    pip install -r requirements.txt
    ```

### 3. Initialize Data & Models
Before running the app, you need to generate synthetic data and train the AI models. Run these commands in order:

1.  **Generate Data**: Creates `demand_history.csv` and `transport_logs.csv`.
    ```powershell
    python utils/data_generator.py
    ```

2.  **Initialize Database**: Sets up `supply_chain.db` (SQLite) for User Auth.
    ```powershell
    python utils/database.py
    ```

3.  **Train AI Models**: Trains LSTM and Regression models and saves them to `models/saved/`.
    ```powershell
    python models/train_models.py
    ```

### 4. Run the Application
Start the Streamlit web interface:
```powershell
streamlit run main.py
```
The app will open automatically in your browser (usually at `http://localhost:8501`).

---

## 📦 Dependencies (`requirements.txt`)
The project uses the following key libraries:
- `streamlit`: For the Web UI.
- `pandas`, `numpy`: For Data Manipulation.
- `scikit-learn`: For Random Forest Regressors (Cost/Delay).
- `tensorflow`: For LSTM Deep Learning (Demand Forecast).
- `plotly`: For Interactive Charts.
- `folium`, `streamlit-folium`: For Maps.
- `matplotlib`: For visualization styling support.
- `sqlalchemy`: For Database interaction.

To install all at once:
```bash
pip install -r requirements.txt
```

---

## 🔑 API Keys
**No external API Keys are required.**
- This project uses **synthetic data generators** (`utils/data_generator.py`) to simulate a realistic supply chain environment.
- Maps are rendered using **OpenStreetMap** (free, via Folium), so no Google Maps API key is needed.

---

## 📂 Project Structure
```
RouteOptix/
│
├── main.py                     # Entry point (Home Page + Chatbot + Auth)
├── requirements.txt            # Python dependencies
├── README.md                   # Documentation
│
├── models/
│   └── train_models.py         # Script to train ML/DL models
│
├── pages/                      # Streamlit Modules
│   ├── 1_Dashboard.py          # Analytics Overview
│   ├── 2_Demand_Forecast.py    # LSTM Forecast & Inventory Opt
│   ├── 3_Route_Optimization.py # ML Prediction & Constraints
│   ├── 4_Multi_Stop_Planner.py # TSP Solver
│   ├── 5_Simulation_Studio.py  # What-If Analysis
│   ├── 6_Risk_and_Performance.py # Heatmaps & Scoring
│   └── 7_Smart_Consolidation.py # Consolidation & Load Opt
│
└── utils/
    ├── data_generator.py       # Syntax Data Creator
    └── database.py             # SQLite Manager
```

## 👤 User Roles (Simulation)
You can simulate different user roles in the application sidebar:
- **Admin**: Full Access.
- **Logistics Manager**: Operations focus.
- **Warehouse Manager**: Inventory focus (Financials hidden).

---
**Developed for Advanced Supply Chain Optimization.**
