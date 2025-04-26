import streamlit as st
import pandas as pd
from io import BytesIO

def run_app():
    st.title("🔧 Machines Report by Number of Service Calls")
    st.write("Upload two files and optionally filter by date range to generate the full report.")

    # File uploaders
    calls_file = st.file_uploader("Upload Service Calls File", type=['xlsx'])
    parts_file = st.file_uploader("Upload Spare Parts File", type=['xlsx'])

    # Date filter checkbox
    filter_dates = st.checkbox("Filter by Date Range")

    if filter_dates:
        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input("Start Date")
        with col2:
            end_date = st.date_input("End Date")

    if st.button("📊 Generate Report"):
        if calls_file and parts_file:
            calls_df = pd.read_excel(calls_file)
            parts_df = pd.read_excel(parts_file)

            # 📋 Show columns to debug
            st.subheader("📋 Columns in Calls File:")
            st.write(calls_df.columns.tolist())

            # 🔥 Try parsing 'ת. פתיחה' safely
            if 'ת. פתיחה' in calls_df.columns:
                calls_df['ת. פתיחה'] = pd.to_datetime(calls_df['ת. פתיחה'], errors='coerce', dayfirst=True)

                # Show number of valid and invalid dates
                st.write(f"✅ Valid dates found: {calls_df['ת. פתיחה'].notna().sum()}")
                st.write(f"❌ Invalid dates (NaT): {calls_df['ת. פתיחה'].isna().sum()}")

                if not calls_df['ת. פתיחה'].isna().all():
                    min_date = calls_df['ת. פתיחה'].min()
                    max_date = calls_df['ת. פתיחה'].max()
                    st.info(f"📅 Dates in Calls File: From {min_date.date()} to {max_date.date()}")
                else:
                    st.error("🚫 No valid opening dates found after parsing! Check your file format.")

                # ✅ Now filter after conversion
                if filter_dates:
                    calls_df = calls_df[
                        (calls_df['ת. פתיחה'] >= pd.Timestamp(start_date)) &
                        (calls_df['ת. פתיחה'] <= pd.Timestamp(end_date))
                    ]

                # ✅ Check if anything left
                if calls_df.empty:
                    st.warning("❗ No service calls found in the selected date range. Please try a different range.")
                    return

                # ========== Now build the report ==========
                # (Continue your report building here)

            else:
                st.error("🚫 'ת. פתיחה' column not found in your Service Calls file!")
                st.stop()

        else:
            st.warning("⚠️ Please upload both required files.")
