import streamlit as st
import pandas as pd
from io import BytesIO

def run_app():
    st.title("🔁 Repeated Calls Analyzer (Technician Breakdown)")

    uploaded_file = st.file_uploader("Upload Service Calls Excel File", type=["xlsx"])
    if uploaded_file:
        st.success("📁 File uploaded.")
        df = pd.read_excel(uploaded_file)
        df.columns = df.columns.str.strip()

        col_map = {
            "call_id": "מס. קריאה",
            "device_id": "מס' מכשיר",
            "call_date": "ת. פתיחה",
            "technician": "לטיפול"
        }

        st.write("📋 Columns in file:", df.columns.tolist())

        if all(col in df.columns for col in col_map.values()):
            df[col_map["call_date"]] = pd.to_datetime(df[col_map["call_date"]], errors="coerce")
            df = df.sort_values(by=[col_map["device_id"], col_map["call_date"]])

            df["Previous Date"] = df.groupby(col_map["device_id"])[col_map["call_date"]].shift(1)
            df["Days Since Last Call"] = (df[col_map["call_date"]] - df["Previous Date"]).dt.days

            repeated_df = df[df["Days Since Last Call"] <= 30].copy()

            st.success(f"✅ Found {len(repeated_df)} repeated calls out of {len(df)} total calls")

            output = BytesIO()
            with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
                for technician in repeated_df[col_map["technician"]].dropna().unique():
                    tech_df = repeated_df[repeated_df[col_map["technician"]] == technician]
                    tech_df.to_excel(writer, sheet_name=str(technician)[:31], index=False)

                summary_df = pd.DataFrame([{
                    "Total Calls": len(df),
                    "Repeated Calls": len(repeated_df),
                    "Repeated %": round(len(repeated_df) / len(df) * 100, 2) if len(df) else 0
                }])
                summary_df.to_excel(writer, sheet_name="Summary", index=False)

            output.seek(0)
            st.download_button(
                label="📥 Download Technician Breakdown Excel",
                data=output,
                file_name="repeated_calls_by_technician.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        else:
            st.error("❌ Missing required columns: מס. קריאה, מס' מכשיר, ת. פתיחה, לטיפול")
