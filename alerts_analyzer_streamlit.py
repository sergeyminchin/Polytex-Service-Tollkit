
import streamlit as st
import pandas as pd
from io import BytesIO
from PIL import Image
import xlsxwriter


# Show logo
try:
    logo = Image.open("logo.png")
    st.image(logo, use_container_width=False)
except:
    st.warning("Logo not found")

st.title("🚨 Polytex Alert Analyzer")

uploaded_file = st.file_uploader("Upload an Excel file", type=["xlsx"])

if uploaded_file:
    try:
        df = pd.read_excel(uploaded_file)
        df.columns = df.columns.str.strip().str.lower()

        required_columns = ["station", "alert", "alert details"]
        if not all(col in df.columns for col in required_columns):
            st.error("Missing required columns: station, alert, or alert details.")
        else:
            unique_alerts = df["alert"].dropna().unique()
            select_all = st.checkbox("Select All Alerts")
            if select_all:
                selected_alerts = sorted(unique_alerts)
            else:
                selected_alerts = st.multiselect("Select alerts to include in the report", sorted(unique_alerts))

            if selected_alerts:
                df_filtered = df[df["alert"].isin(selected_alerts)]

                if not df_filtered.empty:
                    output = BytesIO()
                    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
                        for station in df_filtered["station"].unique():
                            station_data = df_filtered[df_filtered["station"] == station]
                            sheet_name = str(station)[:31]
                            workbook = writer.book
                            worksheet = workbook.add_worksheet(sheet_name)

                            row = 0
                            for alert in selected_alerts:
                                alert_data = station_data[station_data["alert"] == alert]
                                if not alert_data.empty:
                                    summary = alert_data.groupby(["alert", "alert details"]).size().reset_index(name="Count")
                                    worksheet.write(row, 0, f"Alert: {alert}")
                                    row += 1

                                    col_widths = [len(str(col)) for col in summary.columns]
                                    for col_idx, col_name in enumerate(summary.columns):
                                        worksheet.write(row, col_idx, col_name)
                                    row += 1

                                    for record in summary.itertuples(index=False):
                                        for col_idx, value in enumerate(record):
                                            val_str = str(value)
                                            worksheet.write(row, col_idx, val_str)
                                            col_widths[col_idx] = max(col_widths[col_idx], len(val_str))
                                        row += 1

                                    for i, w in enumerate(col_widths):
                                        worksheet.set_column(i, i, w + 2)
                                    row += 2

                    output.seek(0)
                    input_filename = uploaded_file.name.rsplit('.', 1)[0]
                    out_filename = f"{input_filename}_alert_summary.xlsx"

                    st.download_button(
                        label="📥 Download Excel Report",
                        data=output,
                        file_name=out_filename,
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
                else:
                    st.warning("No data available for the selected alerts.")
            else:
                st.info("Please select at least one alert to generate a report.")
    except Exception as e:
        st.error(f"❌ Failed to process file: {e}")