import streamlit as st
import pandas as pd
import io

st.set_page_config(page_title="User Group Exporter", layout="centered")

def run_app():
    st.title("📊 Export or Modify Users File")

    uploaded_file = st.file_uploader("Upload the Users Excel File", type=["xlsx"])

    mode = st.radio(
        "Choose mode:",
        ["Group and Export", "Modify and Export"]
    )

    if uploaded_file:
        df = pd.read_excel(uploaded_file, sheet_name='Users')

        if mode == "Group and Export":
            filter_option = st.radio(
                "Choose filter type:",
                options=["Limit Group", "Department", "Limit Group + Department"]
            )

            if filter_option == "Limit Group + Department":
                df = df.dropna(subset=['Limit Group', 'Department Name'])
                group_cols = ['Limit Group', 'Department Name']
            elif filter_option == "Limit Group":
                df = df.dropna(subset=['Limit Group'])
                group_cols = ['Limit Group']
            else:
                df = df.dropna(subset=['Department Name'])
                group_cols = ['Department Name']

            grouped = df.groupby(group_cols)

            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                for group_keys, group_df in grouped:
                    for col in ["UserID", "CardID"]:
                        if col in group_df.columns:
                            group_df[col] = group_df[col].astype(str).str.zfill(group_df[col].astype(str).str.len().max())
                    if isinstance(group_keys, tuple):
                        sheet_name = "_".join(str(key)[:15] for key in group_keys)
                    else:
                        sheet_name = str(group_keys)[:31]
                    sheet_name = sheet_name.replace('/', '_').replace('\\', '_').replace(':', '_')
                    if len(sheet_name) > 31:
                        sheet_name = sheet_name[:31]
                    group_df.to_excel(writer, sheet_name=sheet_name, index=False)
                    worksheet = writer.sheets[sheet_name]
                    worksheet.set_column('A:Z', None, writer.book.add_format({'num_format': '@'}))

            st.success("✅ Grouped Excel file is ready.")
            st.download_button(
                label="📥 Download Grouped Excel File",
                data=output.getvalue(),
                file_name=f"Users_By_{filter_option.replace(' + ', '_').replace(' ', '')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

        elif mode == "Modify and Export":
            modify_option = st.radio(
                "Choose value type to rename:",
                ["Limit Group", "Department", "Limit Group + Department"]
            )

            if modify_option == "Limit Group":
                original_values = sorted(df['Limit Group'].dropna().unique())
                selected_value = st.selectbox("Select Limit Group to rename:", original_values)
                new_value = st.text_input("Enter new Limit Group name:")
                if new_value:
                    apply_change = st.button("Apply Change")
                    if apply_change:
                        df.loc[df['Limit Group'] == selected_value, 'Limit Group'] = new_value

            elif modify_option == "Department":
                original_values = sorted(df['Department Name'].dropna().unique())
                selected_value = st.selectbox("Select Department to rename:", original_values)
                new_value = st.text_input("Enter new Department name:")
                if new_value:
                    apply_change = st.button("Apply Change")
                    if apply_change:
                        df.loc[df['Department Name'] == selected_value, 'Department Name'] = new_value

            elif modify_option == "Limit Group + Department":
                pairs = df[['Limit Group', 'Department Name']].dropna().drop_duplicates()
                pair_tuples = [tuple(x) for x in pairs.values]
                selected_pair = st.selectbox("Select pair to rename:", pair_tuples)
                new_limit = st.text_input("New Limit Group name:", value=selected_pair[0])
                new_dept = st.text_input("New Department name:", value=selected_pair[1])
                if new_limit and new_dept:
                    apply_change = st.button("Apply Change")
                    if apply_change:
                        df.loc[(df['Limit Group'] == selected_pair[0]) & (df['Department Name'] == selected_pair[1]),
                               ['Limit Group', 'Department Name']] = [new_limit, new_dept]

            if 'apply_change' in locals() and apply_change:
                for col in ["UserID", "CardID"]:
                    if col in df.columns:
                        df[col] = df[col].astype(str).str.zfill(df[col].astype(str).str.len().max())
                output = io.BytesIO()
                with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                    df.to_excel(writer, sheet_name='Users', index=False)
                    worksheet = writer.sheets['Users']
                    worksheet.set_column('A:Z', None, writer.book.add_format({'num_format': '@'}))

                st.success("✅ Modified file is ready.")
                st.download_button(
                    label="📥 Download Modified Excel File",
                    data=output.getvalue(),
                    file_name="Users_Modified.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
