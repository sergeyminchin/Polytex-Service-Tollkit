import streamlit as st
import pandas as pd
from io import BytesIO

def run_app():
    st.title("🔁 Repeated Calls Analyzer (Original Output Format)")

    uploaded_file = st.file_uploader("Upload Service Calls File", type=["xlsx"])
    if uploaded_file:
        df = pd.read_excel(uploaded_file)
        df.columns = df.columns.str.strip()

        # Expected input columns
        call_id_col = "מס. קריאה"
        device_col = "מס' מכשיר"
        date_col = "ת. פתיחה"
        fault_col = "תאור קוד תקלה"
        action_col = "תאור קוד פעולה"

        if not all(col in df.columns for col in [call_id_col, device_col, date_col, fault_col, action_col]):
            st.error("❌ Missing one or more required columns.")
            st.write("📋 Found columns:", df.columns.tolist())
            return

        df[date_col] = pd.to_datetime(df[date_col], errors="coerce")
        df = df.sort_values(by=[device_col, date_col])

        repeated_rows = []
        previous_calls = {}

        for _, row in df.iterrows():
            device_id = row[device_col]
            call_id = row[call_id_col]
            call_date = row[date_col]
            fault = row[fault_col]
            action = row[action_col]

            if pd.isna(call_date):
                continue

            if device_id in previous_calls:
                prev = previous_calls[device_id]
                delta = (call_date - prev["date"]).days
                if delta <= 30:
                    repeated_rows.append({
                        "קריאה ראשונה": prev["call_id"],
                        "תאור תקלה (קריאה ראשונה)": prev["fault"],
                        "תאור קוד פעולה (קריאה ראשונה)": prev["action"],
                        "קריאה חוזרת": call_id,
                        "תאור תקלה (קריאה חוזרת)": fault,
                        "תאור קוד פעולה (קריאה חוזרת)": action,
                        "מס' מכשיר": device_id
                    })

            previous_calls[device_id] = {
                "call_id": call_id,
                "date": call_date,
                "fault": fault,
                "action": action
            }

        repeated_df = pd.DataFrame(repeated_rows)
        st.success(f"Found {len(repeated_df)} repeated call pairs.")
        st.dataframe(repeated_df)

        output = BytesIO()
        with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
            repeated_df.to_excel(writer, sheet_name="Repeated Calls", index=False)
        output.seek(0)

        st.download_button(
            label="📥 Download Excel Output",
            data=output,
            file_name="repeated_calls_structured_output.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
