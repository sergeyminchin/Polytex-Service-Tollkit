
import streamlit as st
import pandas as pd
from io import BytesIO
import os
from PIL import Image


st.title("🔍 RFID Mismatch Analyzer")

uploaded_file = st.file_uploader("Upload an RFID Excel File", type=["xlsx"])

def process_excel(file):
    try:
        df = pd.read_excel(file, engine="openpyxl")

        required_columns = ["RFID", "Item Type Name", "Item Sub Type Name", "Station Name"]
        for col in required_columns:
            if col not in df.columns:
                st.error(f"Missing required column: {col}")
                return None, None

        mismatches = []
        grouped = df.groupby("RFID")
        for rfid, group in grouped:
            if group["Item Type Name"].nunique() > 1 or group["Item Sub Type Name"].nunique() > 1:
                mismatches.append(group)

        result_df = pd.concat(mismatches) if mismatches else pd.DataFrame(columns=df.columns)

        unique_mismatched_rfid = result_df["RFID"].nunique()
        total_transactions = len(df)
        mismatch_percentage = (unique_mismatched_rfid / total_transactions) * 100 if total_transactions > 0 else 0

        summary = {
            "Total Transactions": total_transactions,
            "Mismatched RFID Count": unique_mismatched_rfid,
            "Mismatch Percentage (%)": round(mismatch_percentage, 2)
        }

        return result_df, summary

    except Exception as e:
        st.error(f"Error processing file: {e}")
        return None, None

def generate_excel(result_df, summary):
    output = BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        result_df.to_excel(writer, sheet_name="Mismatched Data", index=False)
        summary_df = pd.DataFrame(list(summary.items()), columns=["Metric", "Value"])
        summary_df.to_excel(writer, sheet_name="Summary", index=False)
    output.seek(0)
    return output

if uploaded_file is not None:
    result_df, summary = process_excel(uploaded_file)

    if result_df is not None:
        st.subheader("📊 Summary")
        st.dataframe(pd.DataFrame([summary]))

        st.subheader("❌ Mismatched Entries")
        st.dataframe(result_df)

        excel_data = generate_excel(result_df, summary)

        # Use the uploaded file name to create output name
        input_filename = uploaded_file.name.rsplit(".", 1)[0]
        download_filename = f"{input_filename}_rfid_mismatch_analysis.xlsx"

        st.download_button(
            label="📥 Download Results as Excel",
            data=excel_data,
            file_name=download_filename,
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
