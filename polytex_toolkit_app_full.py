
import streamlit as st
from PIL import Image
import json
from pathlib import Path
from streamlit_sortables import sort_items

st.set_page_config(page_title="Polytex Service Tools", page_icon="politex.ico", layout="centered")

# ===============================
# 📦 Tool Definitions
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
    "🔎 Service Call Finder": "scfapp",
    "👥 User Group Splitter": "ugs",
    "❓ Help & Guide": "help_app"
}

CONFIG_FILE = Path("visibility_config.json")

# ===============================
# 🔃 Load or Migrate Config

import streamlit as st
from google.oauth2 import service_account
from google.cloud import firestore

# Initialize Firestore from Streamlit secrets
key_dict = st.secrets["firestore"]
credentials = service_account.Credentials.from_service_account_info(key_dict)
db = firestore.Client(credentials=credentials, project=key_dict["project_id"])

# Load config from Firestore
def load_config():
    doc = db.collection("configs").document("tool_config").get()
    return doc.to_dict() if doc.exists else {}

# Save config to Firestore
def save_config(config_data):
    db.collection("configs").document("tool_config").set(config_data)

if "tool_config" not in st.session_state:
    st.session_state.tool_config = {
        "🔁 Repeated Calls Analyzer": {"visible": True, "order": 0},
        "📊 Dashboard Q1 2024 VS Q1 2025": {"visible": True, "order": 1},
        "📈 Universal Dashboard": {"visible": True, "order": 2},
        "🧯 Alerts Filtering": {"visible": True, "order": 3},
        "📦 Duplicates RFID Readings": {"visible": True, "order": 4},
        "🔧 Fixes per Unit": {"visible": True, "order": 5},
        "📦 ServiceCalls_SpareParts": {"visible": True, "order": 6},
        "📂 Service Distribution Transformer": {"visible": True, "order": 7},
        "📦 Spare Parts Usage": {"visible": True, "order": 8},
        "🧠 System Mapper": {"visible": True, "order": 9},
        "🔎 Service Call Finder": {"visible": True, "order": 10},
        "👥 User Group Splitter": {"visible": True, "order": 11},
        "📦 Unreturned Items Detector": {"visible": True, "order": 12},
        "❓ Help & Guide": {"visible": True, "order": 13}
    }
    st.success("✅ Default tool configuration initialized and saved to Firestore!")
}

# ===============================
# 🔐 Admin Login
# ===============================
if "admin" not in st.session_state:
    st.session_state.admin = False

with st.expander("🔑 Admin Login"):
    password = st.text_input("Enter admin password", type="password")
    if password == "polytex123":
        st.session_state.admin = True
        st.success("Admin mode enabled!")

# ⚠️ Temporary block to initialize Firestore config
if st.session_state.admin and st.button("🛠️ Initialize Default Tool Config"):
    save_config({'🔁 Repeated Calls Analyzer': {'visible': True, 'order': 0}, '📊 Dashboard Q1 2024 VS Q1 2025': {'visible': True, 'order': 1}, '📈 Universal Dashboard': {'visible': True, 'order': 2}, '🧯 Alerts Filtering': {'visible': True, 'order': 3}, '📦 Duplicates RFID Readings': {'visible': True, 'order': 4}, '🔧 Fixes per Unit': {'visible': True, 'order': 5}, '📦 ServiceCalls_SpareParts': {'visible': True, 'order': 6}, '📂 Service Distribution Transformer': {'visible': True, 'order': 7}, '📦 Spare Parts Usage': {'visible': True, 'order': 8}, '🧠 System Mapper': {'visible': True, 'order': 9}, '🔎 Service Call Finder': {'visible': True, 'order': 10}, '📦 Unreturned Items Detector': {'visible': True, 'order': 12},
        '❓ Help & Guide': {'visible': True, 'order': 11}})
    st.session_state.tool_config = {
    "🔁 Repeated Calls Analyzer": {"visible": True, "order": 0},
    "📊 Dashboard Q1 2024 VS Q1 2025": {"visible": True, "order": 1},
    "📈 Universal Dashboard": {"visible": True, "order": 2},
    "🧯 Alerts Filtering": {"visible": True, "order": 3},
    "📦 Duplicates RFID Readings": {"visible": True, "order": 4},
    "🔧 Fixes per Unit": {"visible": True, "order": 5},
    "📦 ServiceCalls_SpareParts": {"visible": True, "order": 6},
    "📂 Service Distribution Transformer": {"visible": True, "order": 7},
    "📦 Spare Parts Usage": {"visible": True, "order": 8},
    "🧠 System Mapper": {"visible": True, "order": 9},
    "🔎 Service Call Finder": {"visible": True, "order": 10},
    "👥 User Group Splitter": {"visible": True, "order": 11},
    "📦 Unreturned Items Detector": {"visible": True, "order": 12},
    "❓ Help & Guide": {"visible": True, "order": 13}
},
        '📊 Dashboard Q1 2024 VS Q1 2025': {'visible': True, 'order': 1},
        '📈 Universal Dashboard': {'visible': True, 'order': 2},
        '🧯 Alerts Filtering': {'visible': True, 'order': 3},
        '📦 Duplicates RFID Readings': {'visible': True, 'order': 4},
        '🔧 Fixes per Unit': {'visible': True, 'order': 5},
        '📦 ServiceCalls_SpareParts': {'visible': True, 'order': 6},
        '📂 Service Distribution Transformer': {'visible': True, 'order': 7},
        '📦 Spare Parts Usage': {'visible': True, 'order': 8},
        '🧠 System Mapper': {'visible': True, 'order': 9},
        '🔎 Service Call Finder': {'visible': True, 'order': 10},
        '👥 User Group Splitter': {'visible': True, 'order': 11},
        '📦 Unreturned Items Detector': {'visible': True, 'order': 12},
        '❓ Help & Guide': {'visible': True, 'order': 13}
    }: {'visible': True, 'order': 0}, '📊 Dashboard Q1 2024 VS Q1 2025': {'visible': True, 'order': 1}, '📈 Universal Dashboard': {'visible': True, 'order': 2}, '🧯 Alerts Filtering': {'visible': True, 'order': 3}, '📦 Duplicates RFID Readings': {'visible': True, 'order': 4}, '🔧 Fixes per Unit': {'visible': True, 'order': 5}, '📦 ServiceCalls_SpareParts': {'visible': True, 'order': 6}, '📂 Service Distribution Transformer': {'visible': True, 'order': 7}, '📦 Spare Parts Usage': {'visible': True, 'order': 8}, '🧠 System Mapper': {'visible': True, 'order': 9}, '🔎 Service Call Finder': {'visible': True, 'order': 10}, '📦 Unreturned Items Detector': {'visible': True, 'order': 12},
        '❓ Help & Guide': {'visible': True, 'order': 11}}
    st.success("✅ Default tool configuration initialized and saved to Firestore!")


# ===============================
# 🛠️ Admin Panel: Drag & Visibility
# ===============================
if st.session_state.admin:
    st.subheader("🛠️ Tool Settings: Drag to Reorder & Toggle Visibility")
    current_tools = sorted(st.session_state.tool_config.items(), key=lambda x: x[1]["order"])
    tool_labels = [tool for tool, _ in current_tools]
    sorted_labels = sort_items(tool_labels, direction="vertical")
    for i, tool in enumerate(sorted_labels):
        st.session_state.tool_config[tool]["order"] = i
    for tool in sorted_labels:
        current_val = st.session_state.tool_config[tool]["visible"]
        new_val = st.checkbox(tool, value=current_val, key=f"vis_{tool}")
        if new_val != current_val:
            st.session_state.tool_config[tool]["visible"] = new_val
    if st.button("💾 Save Tool Configuration"):
        save_config(st.session_state.tool_config)
        st.success("✅ Settings saved to Firestore!")

# ===============================
# 🔧 Logo & Title
# ===============================
try:
    logo = Image.open("logo.png")
    st.image(logo, use_container_width=False)
except:
    st.warning("Logo not found.")

st.markdown("<h1 style='font-size: 58px;'>🛠️ Polytex Service Toolkit</h1>", unsafe_allow_html=True)

# ===============================
# 📋 Filter and Sort Tools for Menu
# ===============================
visible_tools = {
    tool: app_options[tool]
    for tool, settings in sorted(st.session_state.tool_config.items(), key=lambda x: x[1]["order"])
    if settings["visible"]
}

if not visible_tools:
    st.warning("No tools enabled. Enable at least one in Admin panel.")
    st.stop()

selected_tool = st.selectbox("Select a Tool", list(visible_tools.keys()))
app_file = visible_tools[selected_tool]

# ===============================
# ▶️ Tool Loader
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


elif app_file == "ugs":
    import ugs
    ugs.run_app()
elif app_file == "scfapp":
    import scfapp
    scfapp.run_app()

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
elif app_file == "nri":
    import nri
    nri.run_app()
