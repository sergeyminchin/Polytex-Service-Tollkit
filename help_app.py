import streamlit as st

def run_app():
    st.title("❓ Help & User Guide")

st.markdown(""" 
Welcome to the **Polytex Service Toolkit** 👋  
This guide provides clear explanations for each tool available in the system.

---

### 🔁 Repeated Calls Analyzer  
Easily spot when the same machine needed service again shortly after a previous visit — or when the same technician made repeated visits, indicating the issue wasn’t fully resolved.  
Just upload your Excel file with the service calls report from Priority (קריאות שירות), and you’ll get a breakdown per technician, with repeat visits clearly highlighted. A summary will also show how often repeated issues occur.

---

### 📊 Dashboard Q1 2024 vs Q1 2025  
This dashboard helps you compare two quarters side-by-side — for example, to see if faults have gone up or which models are causing more trouble over time.  
⚠️ Note: This version is fixed to Q1 of 2024 and 2025 only.  
Use the **Universal Dashboard** tool for flexible time periods.

---

### 📈 Universal Dashboard  
One report — tons of insights.  
With this tool, you can filter and explore your service data however you like: by technician, model, fault, spare parts, and more.  
Upload two Excel files (output of the ServiceCalls_SpareParts tool), label them (e.g., “Q1 2024”) and start comparing.

---

### 🧯 Alerts Filtering  
Got a ton of system alerts? This tool helps you filter out the noise.  
Upload your alert log from PM8 and get a cleaner view of what actually needs attention.  
Just choose the alert types to focus on, and the tool will export an Excel file with a separate tab for each PM8 station.

---

### 📦 Duplicates RFID Readings  
Helps you spot if your RFID system is logging the same item multiple times.  
Upload the transaction report from PM8 (filtered on *Dispenses only*, without *Computerised balance*).  
The tool outputs all duplicate reads and includes a percentage summary.

---

### 🔧 Fixes per Unit  
Analyze how many times each device was repaired — great for identifying chronic issues or understanding lifecycle performance.  
This tool uses the “Fixes per Unit” (תיקונים למכשיר) report from Priority.

---

### 📦 Service Calls & Spare Parts  
This tool analyzes both the “Service Calls” (קריאות שירות) and “Spare Parts Used in Calls” (חלקים שדווחו בקריאות שירות) reports from Priority.  
It provides insights on visits by model, fault codes, and parts usage.  
Want better system mapping? Use **System Mapper** first before running this tool.

---

### 📂 Service Distribution Transformer  
Cleans up system model naming for easier summaries.  
You’ll get a clear breakdown of system types (like DX00, R310, etc.) based on the product code — super useful for logistics and planning.

---

### 📦 Spare Parts Usage  
A dashboard focused entirely on spare part usage.  
Filter by model, technician, or specific parts, and export everything as Excel reports for documentation or analysis.

---

### 🧠 System Mapper  
Different reports use different product codes? No problem.  
This tool “translates” product codes into standard system names like DX00 or R310, based on your rules.  
Upload any or all of the following reports from Priority:
- 🔹 קריאות שירות (Service Calls)  
- 🔹 חלקים שדווחו בקריאות שירות (Spare Parts Used in Calls)  
- 🔹 תיקונים למכשיר (Fixes per Unit)  
You’ll get back files with updated system names — ready for further analysis.

---

📧 For questions or support, contact: **sergeym@polytex.co.il**
""")
