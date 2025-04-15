
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
    "📦 ServiceCalls_SpareParts": "app_final_built_clean",
    "📦 Spare Parts Usage": "parts_dashboard",
    "🧠 System Mapper": "system_mapper_app",
    "📂 Service Distribution Transformer": "distribution_transformer_app"
}

selected_app = st.selectbox("Select a Tool", list(app_options.keys()))

if selected_app:
    app_file = app_options[selected_app]

    if app_file == "repeated_calls":
        import repeated_calls
        repeated_calls.run_app()

    elif app_file == "distribution_transformer_app":
        from distribution_transformer_app import run_transformer_app
        run_transformer_app()

    elif app_file == "parts_dashboard":
        import parts_dashboard
        parts_dashboard.run_app()

    elif app_file == "system_mapper_app":
        import system_mapper_app
        system_mapper_app.run_app()

    else:
        with open(f"{app_file}.py", "r", encoding="utf-8") as f:
            exec(f.read(), globals())

# =======================
# חתימה בסוף הדף - מחוץ לבלוקים
# =======================
st.markdown("---")
st.markdown("🧑‍💻 Developed by: **Sergey Minchin** – **Polytex Service Team**")
st.markdown("📧 sergeym@polytex.co.il")
st.markdown("📅 April 2025")
