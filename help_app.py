import streamlit as st

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
    Tired of inconsistent product codes across different reports? This tool standardizes them for you.
    It automatically translates codes into clear system names (like DX00 or R310) using predefined rules — so all your reports speak the same language.
    📂 Just upload one or more of the following Priority reports:
    🔹 קריאות שירות (Service Calls)
    🔹 חלקים שדווחו בקריאות שירות (Spare Parts Used in Calls)
    🔹 תיקונים למכשיר (Fixes per Unit)

    ✅ The tool returns cleaned-up files with unified system names — ready for analysis or dashboards.

    ---
    For additional support, contact: **sergeym@polytex.co.il**
    """)
