import streamlit as st

st.set_page_config(page_title="Help & User Guide", layout="centered")

def run_app():
    
    st.title("❓ Help & User Guide")

    st.markdown(""" 
    Welcome to the **Polytex Service Toolkit** 👋  
    This guide provides a brief explanation for each tool available in the system.

    ### 🔁 Repeated Calls Analyzer
    Identify repeated service calls within 30 days for the same device, grouped by technician.

    ### 📊 Dashboard Q1 2024 VS Q1 2025
    Compare two Excel service reports and generate dynamic insights per site, device, or failure.

    ### 📈 Universal Dashboard
    Upload and analyze arbitrary Excel reports to extract service statistics.

    ### 🧯 Alerts Filtering
    Analyze technical alerts and generate possible resolutions using known fault/solution mapping.

    ### 📦 Duplicates RFID Readings
    Detect duplicated RFID events in the system logs.

    ### 🔧 Fixes per Unit
    Analyze fixes applied to each device, useful for lifecycle analysis.

    ### 📦 ServiceCalls_SpareParts
    Review spare part usage per unit and technician, including Excel exports.

    ### 📂 Service Distribution Transformer
    Normalize system model naming conventions and summarize quantities.

    ### 📦 Spare Parts Usage
    Full dashboard of spare part usage with filters and visualizations.

    ### 🧩 System Mapper
    Automatically standardize device model codes and descriptions across multiple reports.

    ---
    For additional support, contact: **sergeym@polytex.co.il**
    """)
