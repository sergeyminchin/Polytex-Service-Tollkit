import streamlit as st
import pandas as pd
from io import BytesIO

def run_app():
    st.title("🔁 Repeated Calls by Technician (Tabs per לטיפול)")

    uploaded_file = st.file_uploader("Upload Service Calls Excel File", type=["xlsx"])
    if uploaded_file:
        df = pd.read_excel(uploaded_file)
        df.columns = df.columns.str.strip()

        col_map = {
            "call_id": "מס. קריאה",
            "device_id": "מס' מכשיר",
            "date": "ת. פתיחה",
            "fault": "תאור תקלה",
            "action": "תאור קוד פעולה",
            "tech": "לטיפול"
        }

        if not all(col in df.columns for col in col_map.values()):
            st.error("❌ Missing one or more required columns:")
            st.write("🧾 Found:", df.columns.tolist())
            return

        df[col_map["date"]] = pd.to_datetime(df[col_map["date"]], errors="coerce")
        df = df.sort_values(by=[col_map["device_id"], col_map["date"]])

        output_rows = {}
        summary_rows = []
        total_pairs = 0

        for tech in df[col_map["tech"]].dropna().unique():
            tech_df = df[df[col_map["tech"]] == tech].copy()
            last_call = {}
            repeated = []

            for _, row in tech_df.iterrows():
                device = row[col_map["device_id"]]
                call_id = row[col_map["call_id"]]
                call_date = row[col_map["date"]]
                fault = row[col_map["fault"]]
                action = row[col_map["action"]]

                if pd.isna(call_date):
                    continue

                if device in last_call:
                    prev = last_call[device]
                    days = (call_date - prev["date"]).days
                    if days <= 30:
                        repeated.append({
                            "קריאה ראשונה": prev["call_id"],
                            "תאור תקלה (קריאה ראשונה)": prev["fault"],
                            "תאור קוד פעולה (קריאה ראשונה)": prev["action"],
                            "קריאה חוזרת": call_id,
                            "תאור תקלה (קריאה חוזרת)": fault,
                            "תאור קוד פעולה (קריאה חוזרת)": action,
                            "מס' מכשיר": device
                        })

                last_call[device] = {
                    "call_id": call_id,
                    "date": call_date,
                    "fault": fault,
                    "action": action
                }

            tech_repeats = pd.DataFrame(repeated)
            output_rows[tech] = tech_repeats
            total_pairs += len(tech_repeats)

        st.success(f"📊 Found {total_pairs} repeated call pairs across {len(output_rows)} technicians.")

        output = BytesIO()
        with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
            for tech, df_out in output_rows.items():
                df_out.to_excel(writer, sheet_name=str(tech)[:31], index=False)
                summary_rows.append({
                    "Technician": tech,
                    "Repeated Calls": len(df_out),
                    "Total Calls": len(df[df[col_map["tech"]] == tech]),
                    "Repeated %": round(len(df_out) / len(df[df[col_map["tech"]] == tech]) * 100, 2) if len(df[df[col_map["tech"]] == tech]) > 0 else 0
                })

            summary_df = pd.DataFrame(summary_rows)
            summary_df.to_excel(writer, sheet_name="Summary", index=False)
            output.seek(0)

        st.download_button(
            label="📥 Download Excel File with Technician Tabs",
            data=output,
            file_name="repeated_calls_by_technician_tabs.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
