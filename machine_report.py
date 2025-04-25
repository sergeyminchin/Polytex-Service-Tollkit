import streamlit as st
import pandas as pd
from io import BytesIO

def run_app():
    st.title("📈 דוח מכונות לפי כמות קריאות שירות")
    st.write("העלו שני קבצים ובחרו טווח תאריכים או הפיקו את הדוח לכל התקופה")

# File uploaders
calls_file = st.file_uploader("העלה את קובץ הקריאות", type=['xlsx'])
parts_file = st.file_uploader("העלה את קובץ חלקי החילוף", type=['xlsx'])

# Date filtering
filter_dates = st.checkbox("סנן לפי טווח תאריכים")

if filter_dates:
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("תאריך התחלה")
    with col2:
        end_date = st.date_input("תאריך סיום")

# Generate report button
if st.button("הפק דוח"):
    if calls_file and parts_file:
        calls_df = pd.read_excel(calls_file)
        parts_df = pd.read_excel(parts_file)

        calls_df['ת. פתיחה'] = pd.to_datetime(calls_df['ת. פתיחה'])

        if filter_dates:
            calls_df = calls_df[(calls_df['ת. פתיחה'] >= pd.Timestamp(start_date)) & (calls_df['ת. פתיחה'] <= pd.Timestamp(end_date))]

        summary_with_site = calls_df.groupby('מס\' מכשיר').agg(
            Total_Calls=('מס\' מכשיר', 'size'),
            Site_Name=('תאור האתר', lambda x: x.mode().iloc[0] if not x.mode().empty else 'Unknown Site')
        ).reset_index().sort_values(by='Total_Calls', ascending=False)

        output = BytesIO()
        writer = pd.ExcelWriter(output, engine='xlsxwriter')
        workbook = writer.book
        summary_sheet = workbook.add_worksheet('Summary')
        writer.sheets['Summary'] = summary_sheet

        headers = ['מספר מכשיר', 'כמות קריאות', 'שם אתר']
        for col_num, header in enumerate(headers):
            summary_sheet.write(0, col_num, header)

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
            column_len = max(summary_with_site[headers[col_num].replace('מספר מכשיר', 'מס\' מכשיר')
                                                .replace('כמות קריאות', 'Total_Calls')
                                                .replace('שם אתר', 'Site_Name')].astype(str).map(len).max(), len(header))
            summary_sheet.set_column(col_num, col_num, column_len + 5)

        for machine in summary_with_site['מס\' מכשיר']:
            machine_calls = calls_df[calls_df['מס\' מכשיר'] == machine]
            site_name = summary_with_site[summary_with_site['מס\' מכשיר'] == machine]['Site_Name'].iloc[0]
            call_types = machine_calls['סוג קריאה'].fillna('לא מוגדר').value_counts().reset_index()
            call_types.columns = ['Call Type', 'Count']

            fault_action_details = machine_calls[['מס. קריאה', 'תאור תקלה', 'תאור קוד פעולה']].drop_duplicates()
            fault_action_details.rename(columns={'מס. קריאה': 'מספר קריאה'}, inplace=True)

            relevant_parts = parts_df[parts_df['מספר קריאה'].isin(machine_calls['מס. קריאה']) & (parts_df['כמות בפועל'] > 0)]
            parts_replaced = relevant_parts.groupby(['מק"ט - חלק', 'תאור מוצר - חלק']).agg({'כמות בפועל': 'sum'}).reset_index()
            parts_replaced.columns = ['Part Number', 'Part Description', 'Total Quantity']

            tab_name = f"Machine_{machine}"
            worksheet = workbook.add_worksheet(tab_name)
            writer.sheets[tab_name] = worksheet

            worksheet.write_url('A1', "internal:'Summary'!A1", string="חזרה לטאב Summary")
            worksheet.write('A3', 'אתר:')
            worksheet.write('B3', site_name)
            worksheet.write('A5', 'סוג קריאה וכמות:')

            for idx, (ct, count) in enumerate(call_types.values):
                worksheet.write(6 + idx, 0, ct)
                worksheet.write(6 + idx, 1, count)

            start_row = len(call_types) + 8
            worksheet.write(start_row, 0, 'תיאור תקלה, פעולה ומספר קריאה:')
            fault_action_details.to_excel(writer, sheet_name=tab_name, startrow=start_row + 1, index=False)

            start_row += len(fault_action_details) + 3
            worksheet.write(start_row, 0, 'חלקי חילוף שהוחלפו (כמות בפועל):')
            parts_replaced.to_excel(writer, sheet_name=tab_name, startrow=start_row + 1, index=False)

            # Autofit all columns in the worksheet
            for df in [fault_action_details, parts_replaced]:
                for i, col in enumerate(df.columns):
                    try:
                        col_len = max(df[col].astype(str).map(len).max(), len(str(col)))
                        worksheet.set_column(i, i, col_len + 2)
                    except Exception:
                        pass

        writer.close()
        output.seek(0)

        st.download_button(
            label="📥 הורד את הדוח הסופי",
            data=output,
            file_name="machines_service_calls_report.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    else:
        st.warning("אנא העלה את שני הקבצים כדי להמשיך.")
