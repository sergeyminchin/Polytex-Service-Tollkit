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
Upload your service calls report (קריאות שירות) exported from Priority, and the tool will analyze repeated visits per technician. You’ll get a clear summary of how often repeat calls occur, making it easier to track recurring problems and improve service efficiency.
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
One report — countless insights.
This powerful tool lets you explore your service data exactly how you need: filter by technician, model, fault, spare parts, and more.
Ideal for quarterly or yearly summaries, trend analysis, and pattern detection.
📂 Simply upload two Excel files — the output files from the ServiceCalls_SpareParts tool.
✏️ Label each file (e.g., "Q1 2024") based on the data you're analyzing for a clear side-by-side comparison.
""")

        elif tool == "🧯 Alerts Filtering":
            st.markdown("""
### 🧯 Alerts Filtering  
Drowning in system alerts? This tool helps you cut through the noise!
Upload your PM8 alerts file, choose which alerts you want to focus on, and get a clean, streamlined Excel report.

📌 The output file includes a separate tab for each station from the PM8 site — showing only the alerts you selected for review.
""")

        elif tool == "📦 Duplicates RFID Readings":
            st.markdown("""
### 📦 Duplicates RFID Readings  
Wondering if your RFID system is logging the same item more than once? This tool helps you find out.
Upload the PM8 Transaction Report, filtered to show “Dispenses only” and excluding “Computerised balance” entries.

📌 The output Excel highlights all duplicate readings, along with a clear summary — including counts and percentage of repeated reads.
""")

        elif tool == "🔧 Fixes per Unit":
            st.markdown("""
### 🔧 Fixes per Unit  
Analyze how often each device was repaired — great for identifying chronic issues or understanding lifecycle performance.  
This tool uses the “Fixes per Unit” (תיקונים למכשיר) report from Priority.

✅ Use **System Mapper** first for best accuracy.
""")

        elif tool == "📦 ServiceCalls_SpareParts":
            st.markdown("""
### 📦 Service Calls & Spare Parts  
This tool analyzes data from two Priority reports:
🔹 קריאות שירות (Service Calls)  
🔹 חלקים שדווחו בקריאות שירות (Spare Parts Used in Calls)
It gives you structured insights — like which parts are used most often and which units or models are more problematic.
📊 The output can be used directly in the Universal Dashboard Tool for deeper exploration.
💡 For better system categorization accuracy, use the System Mapper Tool on your original Priority reports before running this tool.
""")

        elif tool == "📂 Service Distribution Transformer":
            st.markdown("""
### 📂 Service Distribution Transformer  
Normalize model names (like DX00, R310).  
Helps logistics by categorizing systems based on code. 

✅ Consider using **System Mapper** instead for better results.
""")

        elif tool == "📦 Spare Parts Usage":
            st.markdown("""
### 📦 Spare Parts Usage  
Dashboard for filtering spare part usage by technician, part, model.  
Use Priority’s “Spare Parts Reported in Service Calls” report.  
Upload the report (חלקים שדווחו בקריאות שירות) as is.
""")

        elif tool == "🧠 System Mapper":
            st.markdown("""
### 🧠 System Mapper  
Standardize product codes to names like DX00 / R310.  
Upload:
- קריאות שירות (Service Calls)  
- חלקים שדווחו בקריאות שירות (Parts used)  
- תיקונים למכשיר (Fixes per Unit)  
Get updated, normalized reports ready for further analysis.
""")

        elif tool == "🔎 Service Call Finder":
            st.markdown("""
### 🔎 Service Call Finder  
Find all the details related to a specific service call — fast.
Search by:
- מספר קריאה (Call Number)
- תאור תקלה (Fault Description)
- תאור קוד פעולה (Action Description)
- Or both תאור תקלה AND תאור קוד פעולה combined.

📂 Upload both the קריאות שירות (Service Calls) and the חלקים שדווחו בקריאות (Parts Used) Excel reports.
📥 Results include model, fault, action, and spare part information, allowing for export to Excel.

✅ Use **System Mapper** first for best accuracy.
""")


        elif tool == "👥 User Group Splitter":
            st.markdown("""
### 👥 User Group Splitter  
Easily manage and export user assignments by department or access group.  
Two main features:
1. **Group and Export** – Automatically create a separate sheet for each Limit Group, Department, or a combination of both.
2. **Modify and Export** – Rename Limit Groups, Departments, or pairings directly from the uploaded Excel and export a clean copy.

📂 Upload the original 'Users' Excel file from PM8 and choose the option that fits your workflow.
            """)

    st.markdown("""---  
📧 For questions or support, contact: **sergeym@polytex.co.il**""")
