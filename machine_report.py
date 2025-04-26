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

            # Convert 'ת. פתיחה' to datetime, dayfirst=True
            calls_df['ת. פתיחה'] = pd.to_datetime(calls_df['ת. פתיחה'], errors='coerce', dayfirst=True)

            # Show available dates to user
            min_date = calls_df['ת. פתיחה'].min()
            max_date = calls_df['ת. פתיחה'].max()
            st.info(f"📅 Dates in Calls File: From {min_date.date()} to {max_date.date()}")

            # ✅ Only now filter if requested
            if filter_dates:
                calls_df = calls_df[
                    (calls_df['ת. פתיחה'] >= pd.Timestamp(start_date)) &
                    (calls_df['ת. פתיחה'] <= pd.Timestamp(end_date))
                ]

            # ✅ Now check if after filtering anything is left
            if calls_df.empty:
                st.warning("❗ No service calls found in the selected date range. Please try a different range.")
                return

            # ========== Continue to report generation ==========
            summary_with_site = calls_df.groupby('מס\' מכשיר').agg(
                Total_Calls=('מס\' מכשיר', 'size'),
                Site_Name=('תאור האתר', lambda x: x.mode().iloc[0] if not x.mode().empty else 'Unknown Site')
            ).reset_index().sort_values(by='Total_Calls', ascending=False)

            output = BytesIO()
            writer = pd.ExcelWriter(output, engine='xlsxwriter')
            workbook = writer.book
            summary_sheet = workbook.add_worksheet('Summary')
            writer.sheets['Summary'] = summary_sheet

            bold_format = workbook.add_format({'bold': True})

            headers = ['Machine ID', 'Total Calls', 'Site Name']
            for col_num, header in enumerate(headers):
                summary_sheet.write(0, col_num, header, bold_format)

            for row_num, (index, row) in enumerate(summary_with_site.iterrows(), start=1):
                machine_id = row['מס\' מכשיר']
                total_calls = row['Total_Calls']
                site_name = row['Site_Name']
                tab_name = f"Machine_{machine_id}"

                link = f"internal:'{tab_name}'!A1"
                summary_sheet.write_url(row_num, 0, link, string=str(machine_id))
                summary_sheet.write(row_num, 1, total_calls)
                summary_sheet.write(row_num, 2, site_name)

            for col_num, header in enumerate(headers):
                summary_sheet.set_column(col_num, col_num, len(header) + 15)

            # ========== Create individual machine tabs ==========
            for machine in summary_with_site['מס\' מכשיר']:
                machine_calls = calls_df[calls_df['מס\' מכשיר'] == machine]
                site_name = summary_with_site[summary_with_site['מס\' מכשיר'] == machine]['Site_Name'].iloc[0]
                call_types = machine_calls['סוג קריאה'].fillna('Not Defined').value_counts().reset_index()
                call_types.columns = ['Call Type', 'Count']

                fault_action_details = machine_calls[['מס. קריאה', 'תאור תקלה', 'תאור קוד פעולה']].drop_duplicates()
                fault_action_details.rename(columns={'מס. קריאה': 'Call Number'}, inplace=True)

                relevant_parts = parts_df[
                    (parts_df['מספר קריאה'].isin(machine_calls['מס. קריאה'])) &
                    (parts_df['כמות בפועל'] > 0)
                ]
                parts_replaced = relevant_parts.groupby(['מק\"ט - חלק', 'תאור מוצר - חלק']).agg({'כמות בפועל': 'sum'}).reset_index()
                parts_replaced.columns = ['Part Number', 'Part Description', 'Total Quantity']

                tab_name = f"Machine_{machine}"
                worksheet = workbook.add_worksheet(tab_name)
                writer.sheets[tab_name] = worksheet

                # Return link to Summary
                worksheet.write_url('A1', "internal:'Summary'!A1", string="🔙 Back to Summary", cell_format=bold_format)

                worksheet.write('A3', 'Site:', bold_format)
                worksheet.write('B3', site_name)

                worksheet.write('A5', 'Call Types and Counts:', bold_format)
                for idx, (ct, count) in enumerate(call_types.values):
                    worksheet.write(6 + idx, 0, ct)
                    worksheet.write(6 + idx, 1, count)

                start_row = len(call_types) + 8
                worksheet.write(start_row, 0, 'Fault Description, Action, and Call Number:', bold_format)
                fault_action_details.to_excel(writer, sheet_name=tab_name, startrow=start_row + 1, index=False)

                start_row += len(fault_action_details) + 3
                worksheet.write(start_row, 0, 'Spare Parts Replaced (Actual Quantity):', bold_format)
                parts_replaced.to_excel(writer, sheet_name=tab_name, startrow=start_row + 1, index=False)

                # Autofit important columns
                for df in [fault_action_details, parts_replaced]:
                    for i, col in enumerate(df.columns):
                        try:
                            col_len = max(df[col].astype(str).map(len).max(), len(str(col)))
                            worksheet.set_column(i, i, col_len + 5)
                        except:
                            pass

            writer.close()
            output.seek(0)

            st.download_button(
                label="📥 Download Final Report",
                data=output,
                file_name="machines_service_calls_report.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        else:
            st.warning("⚠️ Please upload both required files.")
