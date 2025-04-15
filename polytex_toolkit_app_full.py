import streamlit as st
from PIL import Image
import json
from pathlib import Path

# Page config
st.set_page_config(page_title="Polytex Service Tools", page_icon="politex.ico", layout="centered")

# ===============================
# 📦 Available Tools (App Routing)
# ===============================
app_options = {
    "🔁 Repeated Calls Analyzer": "repeated_calls",
    "📊 Dashboard Q1 2024 VS Q1 2025": "dashboard",
    "📈 Universal Dashboard": "Dashboard_un",
    "🧯 Alerts Filtering": "alerts_analyzer_streamlit",
    "📦 Duplicates RFID Readings": "rfid_analysis_streamlit",
    "🔧 Fixes per Unit": "device_fixes_app",
    "📦 ServiceCalls_SpareParts": "app_final_built_clean",
    "📂 Service Distribution Transformer": "distribution_transformer_app",
    "📦 Spare Parts Usage": "parts_dashboard",
    "🧠 System Mapper": "system_mapper_app_final",
    "❓ Help & Guide": "help_app"
}

# ===============================
# 🔐 Tool Visibility Config (Persisted)
# ===============================
CONFIG_FILE = Path("visibility_config.json")

# Load visibility settings from file or set all to True
if CONFIG_FILE.exists():
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        tool_visibility = json.load(f)
else:
    tool_visibility = {tool: True for tool in app_options}

# Initialize session state with visibility
if "tool_visibility" not in st.session_state:
    st.session_state.tool_visibility = tool_visibility

# ===============================
# 🔐 Admin Login Panel
# ===============================
if "admin" not in st.session_state:
    st.session_state.admin = False

with st.expander("🔑 Admin Login"):
    password = st.text_input("Enter admin password", type="password")
    if password == "polytex123":
        st.session_state.admin = True
        st.success("Admin mode enabled!")

# Admin settings toggle panel
if st.session_state.admin:
    st.subheader("🛠️ Toggle Tool Visibility")
    changed = False
    for key in st.session_state.tool_visibility:
        new_val = st.checkbox(key, value=st.session_state.tool_visibility[key])
        if new_val != st.session_state.tool_visibility[key]:
            st.session_state.tool_visibility[key] = new_val
            changed = True

    if changed:
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(st.session_state.tool_visibility, f, ensure_ascii=False, indent=2)
        st.success("Visibility settings saved!")

# ===============================
# 🔧 Logo and Title
# ===============================
try:
    logo = Image.open("logo.png")
    st.image(logo, use_container_width=False)
except:
    st.warning("Logo not found.")

st.title("🛠️ Polytex Service Toolkit")

# ===============================
# 🎛️ Filter Visible Tools
# ===============================
visible_apps = {k: v for k, v in app_options.items() if st.session_state.tool_visibility.get(k, False)}

if not visible_apps:
    st.warning("No tools available. Please log in as admin to enable tools.")
    st.stop()

selected_app = st.selectbox("Select a Tool", list(visible_apps.keys()))
app_file = visible_apps[selected_app]

# ===============================
# ▶️ Load Selected App
# ===============================
if app_file == "repeated_calls":
    import repeated_calls
    repeated_calls.run_app()

elif app_file == "distribution_transformer_app":
    from distribution_transformer_app import run_transformer_app
    run_transformer_app()

elif app_file == "parts_dashboard":
    import parts_dashboard
    parts_dashboard.run_app()

elif app_file == "system_mapper_app_final":
    import system_mapper_app_final as system_mapper_app
    system_mapper_app.run_app()

elif app_file == "help_app":
    import help_app
    help_app.run_app()

else:
    with open(f"{app_file}.py", "r", encoding="utf-8") as f:
        exec(f.read(), globals())

# ===============================
# Footer
# ===============================
st.markdown("---")
st.markdown("🧑‍💻 Developed by: **Sergey Minchin** – **Polytex Service Team**")
st.markdown("📧 sergeym@polytex.co.il")
st.markdown("📅 April 2025")
