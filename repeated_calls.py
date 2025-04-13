import streamlit as st
import pandas as pd
from io import BytesIO

def run_app():
    st.title("🔁 Repeated Service Calls Analyzer (Final Version)")

    uploaded_file = st.file_uploader("Upload the Service Calls Excel File", type=["xlsx"])
    if uploaded_file is not None:
        df = pd.read_excel(uploaded_file)

        call_id_col = "מס. קריאה"
        device_id_col = "מס' מכשיר"
        date_col = "ת. פתיחה"

        if call_id_col in df.columns and device_id_col in df.columns and date_col in df.columns:
            df[date_col] = pd.to_datetime(df[date_col], errors="coerce")
            df = df.sort_values(by=[device_id_col, date_col])

            df["Previous Date"] = df.groupby(device_id_col)[date_col].shift(1)
            df["Days Since Last Call"] = (df[date_col] - df["Previous Date"]).dt.days

            repeated_df = df[df["Days Since Last Call"] <= 30].copy()

            st.subheader("🔁 Repeated Calls Detected (within 30 days for the same device)")
            st.dataframe(repeated_df)

            output = BytesIO()
            with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
                repeated_df.to_excel(writer, sheet_name="Repeated Calls", index=False)
            output.seek(0)

            st.download_button(
                label="📥 Download Excel Report",
                data=output,
                file_name="repeated_calls_output.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        else:
            st.error("❌ The file is missing one of the required columns: 'מס. קריאה', 'מס' מכשיר', or 'ת. פתיחה'")
