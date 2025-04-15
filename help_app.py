import streamlit as st

def run_app():
    st.title("❓ Help & User Guide")

    tool_visibility = st.session_state.get("tool_visibility", {})

    st.markdown("Welcome to the **Polytex Service Toolkit** 👋  \nThis guide provides clear explanations for each tool available in the system.\n---")

    if tool_visibility.get("🔁 Repeated Calls Analyzer"):
        st.markdown("""
### 🔁 Repeated Calls Analyzer  
Easily spot when the same machine needed service again shortly after a previous visit — or when the same technician made repeated visits, indicating the issue wasn’t fully resolved.  
Upload your Excel file with the service calls report from Priority (קריאות שירות), and get a breakdown per technician with repeat visits highlighted.
""")

    if tool_visibility.get("📊 Dashboard Q1 2024 VS Q1 2025"):
        st.markdown("""
### 📊 Dashboard Q1 2024 vs Q1 2025  
Compare two quarters side-by-side to see if faults have gone up or which models are more problematic.  
⚠️ Fixed to Q1 of 2024 and 2025. Use **Universal Dashboard** for flexible dates.
""")

    if tool_visibility.get("📈 Universal Dashboard"):
        st.markdown("""
### 📈 Universal Dashboard  
Explore your service data: by technician, model, fault, spare parts, and more.  
Upload two Excel files (output of the ServiceCalls_SpareParts tool), label them (e.g., “Q1 2024”) and compare.
""")

    if tool_visibility.get("🧯 Alerts Filtering"):
        st.markdown("""
### 🧯 Alerts Filtering  
Filter out noise from technical alerts.  
Upload your alert log from PM8 and generate Excel exports per PM8 station.
""")

    if tool_visibility.get("📦 Duplicates RFID Readings"):
        st.markdown("""
### 📦 Duplicates RFID Readings  
Detect duplicated RFID events in PM8 logs.  
Use *Dispenses only* reports, excluding *Computerised balance*.
""")

    if tool_visibility.get("🔧 Fixes per Unit"):
        st.markdown("""
### 🔧 Fixes per Unit  
Analyze device repair frequency — useful for lifecycle evaluation or chronic failure tracking.
""")

    if tool_visibility.get("📦 ServiceCalls_SpareParts"):
        st.markdown("""
### 📦 Service Calls & Spare Parts  
Analyze “Service Calls” and “Spare Parts Used in Calls” from Priority.  
See visits by model, fault code, and parts.  
✅ Use **System Mapper** first for cleaner mapping.
""")

    if tool_visibility.get("📂 Service Distribution Transformer"):
        st.markdown("""
### 📂 Service Distribution Transformer  
Normalize model names (like DX00, R310).  
Helps logistics by categorizing systems based on code.  
✅ Consider using **System Mapper** instead for better results.
""")

    if tool_visibility.get("📦 Spare Parts Usage"):
        st.markdown("""
### 📦 Spare Parts Usage  
Dashboard for filtering spare part usage by technician, part, model.  
Use Priority’s “Spare Parts Used in Calls” report.  
✅ Use **System Mapper** first for best accuracy.
""")

    if tool_visibility.get("🧠 System Mapper"):
        st.markdown("""
### 🧠 System Mapper  
Standardize product codes to names like DX00 / R310.  
Upload:
- קריאות שירות (Service Calls)  
- חלקים שדווחו בקריאות שירות (Parts used)  
- תיקונים למכשיר (Fixes per Unit)  
Get updated, normalized reports ready for further analysis.
""")

    st.markdown("""
---
📧 For questions or support, contact: **sergeym@polytex.co.il**
""")
