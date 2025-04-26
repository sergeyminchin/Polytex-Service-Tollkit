import streamlit as st
import pandas as pd
from io import BytesIO

# 🛠 HELPER FUNCTIONS
def autofit_columns(worksheet, dataframe, padding=5):
    for i, col in enumerate(dataframe.columns):
        try:
            max_length = max(
                dataframe[col].astype(str).map(len).max(),
                len(str(col))
            )
            worksheet.set_column(i, i, max_length + padding)
        except Exception:
            pass

def write_simple_table(worksheet, start_row, title, dataframe, writer):
    bold_format = writer.book.add_format({'bold': True})
    worksheet.write(start_row, 0, title, bold_format)
    dataframe.to_excel(writer, sheet_name=worksheet.name, startrow=start_row + 1, index=False)
    autofit_columns(worksheet, dataframe)
    return start_row + len(dataframe) + 3

# 💻 MAIN APP
def run_app():
    st.title("🔧 Machines Report by Number of Service Calls")
    st.write("Upload two files and optionally filter by date range to generate the full report.")

    calls_file = st.file_uploader("Upload Service Calls File", type=['xlsx'])
    parts_file = st.file_uploader("Upload Spare Parts File", type=['xlsx'])

    if calls_file and parts_file:
        calls_df = pd.read_excel(calls_file)
        parts_df = pd.read_excel(parts_file)

        # Parse opening dates
        calls_df['ת. פתיחה'] = pd.to_datetime(calls_df['ת. פתיחה'], errors='coerce', dayfirst=True)

        # Available dates
        min_date = calls_df['ת. פתיחה'].min()
        max_date = calls_df['ת. פתיחה'].max()
        st.info(f"🗕️ Dates in Calls File: From {min_date.date()} to {max_date.date()}")

        # Date filter
        filter_dates = st.checkbox("Filter by Date Range", value=True)

        if filter_dates:
            col1, col2 = st.columns(2)
            with col1:
                start_date = st.date_input("Start Date", value=min_date.date(), min_value=min_date.date(), max_value=max_date.date())
            with col2:
                end_date = st.date_input("End Date", value=max_date.date(), min_value=min_date.date(), max_value=max_date.date())

            start_date = pd.to_datetime(start_date)
            end_date = pd.to_datetime(end_date)

            calls_df = calls_df[(calls_df['ת. פתיחה'] >= start_date) & (calls_df['ת. פתיחה'] <= end_date)]

        if calls_df.empty:
            st.warning("❗️ No service calls found in the selected date range.")
            return

        if st.button("📊 Generate Report"):
            output = BytesIO()
            writer = pd.ExcelWriter(output, engine='xlsxwriter')
            workbook = writer.book

            summary_with_site = calls_df.groupby('מס\' מכשיר').agg(
                Total_Calls=('מס\' מכשיר', 'size'),
                Site_Name=('תאור האתר', lambda x: x.mode().iloc[0] if not x.mode().empty else 'Unknown Site')
            ).reset_index().sort_values(by='Total_Calls', ascending=False)

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
                if header == 'Site Name':
                    summary_sheet.set_column(col_num, col_num, len(header) + 30)
                else:
                    summary_sheet.set_column(col_num, col_num, len(header) + 10)

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

                worksheet.write_url('A1', "internal:'Summary'!A1", string="🖙 Back to Summary", cell_format=bold_format)
                worksheet.write('A3', 'Site:', bold_format)
                worksheet.write('B3', site_name, bold_format)
                worksheet.write('A5', 'Call Types and Counts:', bold_format)

                for idx, (ct, count) in enumerate(call_types.values):
                    worksheet.write(6 + idx, 0, ct)
                    worksheet.write(6 + idx, 1, count)

                start_row = len(call_types) + 8

                start_row = write_simple_table(worksheet, start_row, 'Fault Description, Action, and Call Number:', fault_action_details, writer)
                start_row = write_simple_table(worksheet, start_row, 'Spare Parts Replaced (Actual Quantity):', parts_replaced, writer)

            writer.close()
            output.seek(0)

            st.download_button(
                label="👅 Download Final Report",
                data=output,
                file_name="machines_service_calls_report.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
    else:
        st.warning("⚠️ Please upload both required files.")

if __name__ == "__main__":
    run_app()
