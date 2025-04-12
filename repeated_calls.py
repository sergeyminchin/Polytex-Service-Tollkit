
import streamlit as st
import pandas as pd
from collections import defaultdict
from io import BytesIO
from openpyxl import load_workbook
from openpyxl.utils import get_column_letter
from openpyxl.styles import Font

st.title("🔁 Repeated Service Calls Analyzer")

uploaded_file = st.file_uploader("Upload the Service Calls Report (.xlsx)", type=["xlsx"])

def fuzzy_column_match(columns):
    mapping = {
        "call_id": None,
        "device_id": None,
        "call_date": None
    }
    for col in columns:
        c = col.strip().replace(" ", "").replace("'", "")
        if "קריאה" in c and ("מס" in c or "מספר" in c):
            mapping["call_id"] = col
        elif "מכשיר" in c:
            mapping["device_id"] = col
        elif "תאריך" in c and "קריאה" in c:
            mapping["call_date"] = col
    return mapping

def analyze_repeat_calls(df, call_id_col, device_id_col, date_col):
    df[date_col] = pd.to_datetime(df[date_col], errors="coerce")
    df = df.sort_values(by=[device_id_col, date_col])

    device_calls = defaultdict(list)
    for _, row in df.iterrows():
        device_id = row[device_id_col]
        call_id = row[call_id_col]
        open_date = row[date_col]

        if pd.isna(open_date):
            continue

        if device_calls[device_id]:
            last_call = device_calls[device_id][-1]
            if (open_date - last_call["date"]).days <= 30:
                last_call["repeats"].append({
                    "call_id": call_id,
                    "date": open_date
                })

        device_calls[device_id].append({
            "call_id": call_id,
            "date": open_date,
            "repeats": []
        })

    total_calls = len(df)
    repeated_data = []

    for calls in device_calls.values():
        for call in calls:
            for rpt in call["repeats"]:
                repeated_data.append({
                    "קריאה ראשונה": call["call_id"],
                    "תאריך קריאה ראשונה": call["date"],
                    "קריאה חוזרת": rpt["call_id"],
                    "תאריך קריאה חוזרת": rpt["date"],
                    "מספר מכשיר": device_id
                })

    repeated_df = pd.DataFrame(repeated_data)
    summary = {
        "Total Calls": total_calls,
        "Repeated Calls": len(repeated_df),
        "Percentage Repeated": f"{(len(repeated_df) / total_calls * 100):.2f}%" if total_calls else "0%"
    }

    return repeated_df, summary

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    st.write("📋 Detected Columns:", df.columns.tolist())

    matched = fuzzy_column_match(df.columns)
    missing = [k for k, v in matched.items() if v is None]

    if missing:
        st.error(f"Missing required columns: {', '.join(missing)}")
    else:
        repeated_df, summary = analyze_repeat_calls(df, matched["call_id"], matched["device_id"], matched["call_date"])

        st.subheader("📊 Summary")
        st.write(summary)

        st.subheader("🔁 Repeated Calls")
        st.dataframe(repeated_df)

        output = BytesIO()
        with pd.ExcelWriter(output, engine="openpyxl") as writer:
            repeated_df.to_excel(writer, index=False, sheet_name="Repeated Calls")
            pd.DataFrame([summary]).to_excel(writer, index=False, sheet_name="Summary")
        output.seek(0)

        st.download_button(
            label="📥 Download Excel Report",
            data=output,
            file_name="repeated_calls_report.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
