import streamlit as st
import utils.database as db
import time

st.set_page_config(page_title="RouteOptix: Intelligent Supply Chain", layout="wide")

# Session State Init
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'username' not in st.session_state:
    st.session_state['username'] = None

def login_page():
    st.title("🔐 RouteOptix Login")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Login")
        username = st.text_input("Username", key="login_user")
        password = st.text_input("Password", type="password", key="login_pw")
        if st.button("Login"):
            if db.login_user(username, password):
                st.session_state['logged_in'] = True
                st.session_state['username'] = username
                st.success("Logged in successfully!")
                st.rerun()
            else:
                st.error("Invalid username or password")
                
    with col2:
        st.subheader("Register")
        new_user = st.text_input("Username", key="reg_user")
        new_pw = st.text_input("Password", type="password", key="reg_pw")
        if st.button("Register"):
            if new_user and new_pw:
                if db.register_user(new_user, new_pw):
                    st.success("Registration successful! Please login.")
                else:
                    st.error("Username already exists.")
            else:
                st.warning("Please fill all fields.")

def main_dashboard():
    st.sidebar.title(f"Welcome, {st.session_state['username']}")
    if st.sidebar.button("Logout"):
        st.session_state['logged_in'] = False
        st.session_state['username'] = None
        st.rerun()
        
    st.title("🚛 Intelligent Supply Chain Optimization")
    
    # --- RBAC Mock ---
    role = st.sidebar.selectbox("User Role", ["Admin", "Logistics Manager", "Warehouse Manager"])
    st.sidebar.info(f"Logged in as: **{role}**")
    
    if role == "Warehouse Manager":
        st.warning("View Restricted: Financial modules hidden.")
    
    st.markdown("""
    Welcome to the **RouteOptix** Intelligent Supply Chain System.
    
    This platform leverages **Machine Learning** and **Deep Learning** to optimize your logistics:
    
    *   **📊 Dashboard**: Overview of supply chain metrics.
    *   **📈 Demand Forecast**: Deep Learning (LSTM) models to predict future product demand.
    *   **🚀 Route Optimization**: ML Regression to predict cost & delays and find the best transport mode.
    *   **🧪 Simulation**: Analyze "What-If" scenarios.
    *   **radar Risk**: Monitor risk heatmaps and carrier scores.
    
    👈 **Select a module from the sidebar to get started.**
    """)
    
    st.info("System Status: Online | Models: Loaded | Database: Connected")
    
    # --- AI Decision Support Assistant ---
    st.markdown("---")
    st.subheader("🤖 AI Decision Assistant")
    
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # User input
    if prompt := st.chat_input("Ask about logistics (e.g., 'Best carrier for fragile items?', 'Cost to ship to NY?')..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Simple Logic Response
        response = "I'm analyzing your request... "
        if "cost" in prompt.lower():
            response += "Shipping costs are trending slightly higher due to fuel surges. Check the Simulation Studio for details."
        elif "carrier" in prompt.lower():
            response += "Based on recent scores, 'DHL' has the highest reliability (98%) for Air freight."
        elif "risk" in prompt.lower():
            response += "Current high-risk zones include the Los Angeles Port area due to congestion."
        else:
            response += "I can help optimize routes or forecast demand. Try checking the specific pages in the sidebar!"
            
        st.session_state.messages.append({"role": "assistant", "content": response})
        with st.chat_message("assistant"):
            st.markdown(response)

if __name__ == "__main__":
    if not st.session_state['logged_in']:
        login_page()
    else:
        main_dashboard()
