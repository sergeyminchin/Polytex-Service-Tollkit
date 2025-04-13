
import streamlit as st
from PIL import Image

# Set branding
st.set_page_config(page_title="Polytex Service Tools", page_icon="politex.ico", layout="centered")

# Logo display
try:
    logo = Image.open("logo.png")
    st.image(logo, use_container_width=False)
except:
    st.warning("Logo not found.")

st.title("🛠️ Polytex Service Toolkit")

# App selection
app_options = {
    "🔁 Repeated Calls Analyzer": "repeated_calls",
    "📊 Dashboard Q1 2024 VS Q1 2025": "dashboard",
    "📈 Universal Dashboard": "Dashboard_un",
    "🧯 Alerts Filtering": "alerts_analyzer_streamlit",
    "📦 Duplicates RFID Readings": "rfid_analysis_streamlit",
    "🔧 Fixes per Unit": "device_fixes_app",
    "📦 ServiceCalls_SpareParts": "app_final_built_clean"
}

selected_app = st.selectbox("Select a Tool", list(app_options.keys()))

# Dynamic module loading
if selected_app:
    app_file = app_options[selected_app]
    if app_file == "repeated_calls":
        import repeated_calls
        repeated_calls.run_app()
    else:
        with open(f"{app_file}.py", "r", encoding="utf-8") as f:
            exec(f.read(), globals())
