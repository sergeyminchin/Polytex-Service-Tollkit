
import streamlit as st
import pandas as pd
from io import BytesIO

st.title("🔁 Repeated Service Calls Analyzer")

uploaded_file = st.file_uploader("Upload Excel File", type=["xlsx"])
if uploaded_file is not None:
    df = pd.read_excel(uploaded_file)
    df.columns = df.columns.str.strip()

    # Flexible column matching
    call_id_col = None
    device_col = None
    date_col = None

    for col in df.columns:
        col_clean = col.replace(" ", "").replace("'", "")
        if "קריאה" in col_clean and ("מס" in col_clean or "מספר" in col_clean):
            call_id_col = col
        if "מכשיר" in col_clean:
            device_col = col
        if "תאריך" in col_clean:
            date_col = col

    if call_id_col and device_col and date_col:
        df[date_col] = pd.to_datetime(df[date_col], errors='coerce')
        df = df.sort_values(by=[device_col, date_col])

        df['Previous Date'] = df.groupby(device_col)[date_col].shift(1)
        df['Days Since Last Call'] = (df[date_col] - df['Previous Date']).dt.days

        repeated_df = df[df['Days Since Last Call'] <= 30].copy()

        st.subheader("🔁 Repeated Calls Detected (within 30 days for same device)")
        st.dataframe(repeated_df)

        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            repeated_df.to_excel(writer, index=False, sheet_name='Repeated Calls')
        output.seek(0)

        st.download_button(
            label="📥 Download Result as Excel",
            data=output,
            file_name="repeated_calls_output.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    else:
        st.error("❌ The file is missing one of the required columns: 'מס' קריאה', 'מספר מכשיר', or 'תאריך קריאה'")
