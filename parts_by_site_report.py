import streamlit as st
import pandas as pd
from io import BytesIO

def run_app():
    st.set_page_config(page_title="Spare Parts by Site", layout="centered")
    st.title("📦 Spare Parts Report by Site")

    st.markdown("Upload the **Parts Report** and **Service Calls Report** to generate a site-based summary of replaced parts.")

    parts_file = st.file_uploader("📄 Upload Parts Report", type=["xlsx"])
    calls_file = st.file_uploader("📄 Upload Service Calls Report", type=["xlsx"])

    if parts_file and calls_file:
        parts_df = pd.read_excel(parts_file)
        calls_df = pd.read_excel(calls_file)

        # Merge based on Service Call Number
        merged_df = parts_df.merge(
            calls_df[['מס. קריאה', 'תאור האתר']],
            left_on='מספר קריאה',
            right_on='מס. קריאה',
            how='left'
        )

        # Clean and rename columns
        merged_df = merged_df.rename(columns={
            'מספר קריאה': 'Service Call Number',
            'תאור האתר': 'Site Name',
            'מק"ט - חלק': 'Part Number',
            'תאור מוצר - חלק': 'Part Description',
            'כמות בפועל': 'Quantity Used'
        })

        # Drop rows with no site or non-positive quantity
        merged_df = merged_df.dropna(subset=['Site Name'])
        merged_df = merged_df[merged_df['Quantity Used'] > 0]

        # Site selection
        site_options = sorted(merged_df['Site Name'].unique())
        st.markdown("### 🏥 Site Selection")
        all_sites = st.checkbox("Select All Sites", value=True)

        if all_sites:
            selected_sites = site_options
        else:
            selected_sites = st.multiselect("Choose Sites", options=site_options)

        st.caption(f"✅ {len(selected_sites)} site(s) selected")

        # Report generation
        if selected_sites and st.button("📊 Create Report"):
            output = BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                for site in selected_sites:
                    site_df = merged_df[merged_df['Site Name'] == site]
                    summary_df = site_df.groupby(
                        ['Part Number', 'Part Description'], as_index=False
                    )['Quantity Used'].sum().sort_values(by='Quantity Used', ascending=False)

                    sheet_name = site[:31]
                    summary_df.to_excel(writer, sheet_name=sheet_name, index=False)

                    # Auto-adjust column widths
                    worksheet = writer.sheets[sheet_name]
                    for idx, col in enumerate(summary_df.columns):
                        max_len = max(
                            summary_df[col].astype(str).map(len).max(),
                            len(str(col))
                        ) + 1
                        worksheet.set_column(idx, idx, max_len)

            st.success("✅ Report created. Click below to download.")
            st.download_button(
                label="📥 Download Excel Report",
                data=output.getvalue(),
                file_name="Spare_Parts_By_Site_Report.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

if __name__ == "__main__":
    run_app()
