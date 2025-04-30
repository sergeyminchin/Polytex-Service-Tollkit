import streamlit as st

def run_app():
    st.title("❓ Help & User Guide")

    tool_config = st.session_state.get("tool_config", {})
    sorted_visible_tools = [
        (tool, settings) for tool, settings in sorted(tool_config.items(), key=lambda x: x[1]["order"])
        if settings.get("visible", True)
    ]

    st.markdown("Welcome to the **Polytex Service Toolkit** 👋  \nThis guide provides clear explanations for each tool available in the system.\n---")

    for tool, _ in sorted_visible_tools:
        if tool == "🔁 Repeated Calls Analyzer":
            st.markdown("""
### 🔁 Repeated Calls Analyzer  
Quickly identify when a machine required service again shortly after a previous visit — or when the same technician is repeatedly called to the same unit. These patterns often point to unresolved issues that need further attention.

Upload your service calls report (קריאות שירות) exported from Priority, and the tool will analyze repeated visits per technician.

You’ll get a clear summary of how often repeat calls occur, making it easier to track recurring problems and improve service efficiency.
""")

        elif tool == "📦 Unreturned Items Detector":
            st.markdown("""
### 📦 Unreturned Items Detector  
Find out who dispensed items and didn’t return them — within a selected timeframe.

Choose your analysis period (1 week, 1 month, etc.) and get:
- A sheet with all unreturned items by user
- A summary sheet with total count
- A detailed breakdown by item type/subtype

Supports both Excel and CSV exports from the PM8 Transaction Report.  
✅ Output preserves original ID formatting and includes autofit for readability.
""")

        elif tool == "📊 Dashboard Q1 2024 VS Q1 2025":
            st.markdown("""
### 📊 Dashboard Q1 2024 vs Q1 2025  
Easily compare service trends between Q1 2024 and Q1 2025 side-by-side.

This dashboard helps you spot increases in faults, identify which models are becoming more problematic, and understand overall service patterns over time.  
⚠️ Fixed to Q1 of 2024 and 2025. Use **Universal Dashboard** for flexible dates.
""")

        elif tool == "📈 Universal Dashboard":
            st.markdown("""
### 📈 Universal Dashboard  
This powerful tool lets you explore your service data exactly how you need: filter by technician, model, fault, spare parts, and more.

📂 Upload two Excel files — the output files from the ServiceCalls_SpareParts tool.

✏️ Label each file (e.g., "Q1 2024") based on the data you're analyzing.
""")

        elif tool == "🧯 Alerts Filtering":
            st.markdown("""
### 🧯 Alerts Filtering  
Upload your PM8 alerts file, choose the alerts to keep, and generate a streamlined Excel report.

📌 Each tab corresponds to a station showing only the selected alerts.
""")

        elif tool == "📦 Duplicates RFID Readings":
            st.markdown("""
### 📦 Duplicates RFID Readings  
Upload the PM8 Transaction Report (dispenses only, no computerized balances).

🧐 Detect duplicate RFID reads and get an Excel summary with frequency and percentages.
""")

        elif tool == "🔧 Fixes per Unit":
            st.markdown("""
### 🔧 Fixes per Unit  
Analyze how often each device was repaired.

✅ Requires the “Fixes per Unit” (תיקונים למכשיר) report from Priority.
""")

        elif tool == "📦 ServiceCalls_SpareParts":
            st.markdown("""
### 📦 Service Calls & Spare Parts  
Uses data from:
- קריאות שירות (Service Calls)
- חלקים שדווחו בקריאות שירות (Parts Used)

🎯 Understand service costs, part usage, and call distributions.  
💡 Use System Mapper first for the uploaded files to ensure the best accuracy.
""")

        elif tool == "📂 Service Distribution Transformer":
            st.markdown("""
### 📂 Service Distribution Transformer  
Normalize system models like DX00, R310.

✅ Useful, but I prefer System Mapper when possible.
""")

        elif tool == "📦 Spare Parts Usage":
            st.markdown("""
### 📦 Spare Parts Usage  
Upload Priority's “Parts Used in Service Calls” and filter by part, model, or technician.

💡 Use System Mapper first for the uploaded files to ensure the best accuracy.
""")

        elif tool == "🧠 System Mapper":
            st.markdown("""
### 🧠 System Mapper  
Standardize model names across reports.

Input:
- קריאות שירות
- חלקים שדווחו בקריאות שירות
- תיקונים למכשיר

Output: clean, normalized versions for analysis.
""")

        elif tool == "🔎 Service Call Finder":
            st.markdown("""
### 🔎 Service Call Finder  
Quickly locate any service call details by:
- מספר קריאה
- תאור תקלה
- תאור קוד פעולה

Output includes call, model, fault, and part info.
""")

        elif tool == "👥 User Group Splitter":
            st.markdown("""
### 👥 User Group Splitter  
Upload the PM8 'Users' Excel file.

Two modes:
- Group and Export (by Department / Limit Group)
- Modify and Export (rename and export the updated file)
""")
        elif tool == "🔧 Machine Report Generator":
            st.markdown("""
### 🔧 Machine Report Generator  
Generate a full Excel report showing which machines had the most service calls, and analyze what happened.

🧾 Upload:
- קריאות שירות (Service Calls)
- חלקים שדווחו בקריאות (Spare Parts Used in Calls)

📊 For each machine:
- Total number of calls
- Site name
- Breakdown of call types
- List of fault descriptions and actions
- All spare parts replaced, including quantity

🧭 Click any machine in the summary tab to jump to its detailed page.  
🔁 Each sheet has a link to return to the summary.
💡 Use System Mapper first for the uploaded files to ensure the best accuracy.
""")

elif tool == "📦 Spare Parts by Site":
    st.markdown("""
### 📦 Spare Parts by Site  
Upload two reports:
- חלקים שדווחו בקריאות שירות (Parts Used)
- קריאות שירות (Service Calls)

Choose one or more sites to analyze.  
📥 The output Excel file includes a separate sheet for each selected site, listing the parts used and their quantities.

✅ Autofit column widths  
✅ Hebrew/Unicode support  
✅ Designed for detailed site-based spare part tracking
""")


    st.markdown("""---  
📧 Contact support: **sergeym@polytex.co.il**""")
