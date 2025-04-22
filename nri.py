import streamlit as st
import pandas as pd
import io
from datetime import datetime, timedelta

def classify_transactions(df):
    df["CreatedDate"] = pd.to_datetime(df["CreatedDate"], errors="coerce")
    df = df.dropna(subset=["CreatedDate"])

    # Convert quantity fields to numeric before calculation
    df["QtyBalAfter"] = pd.to_numeric(df["QtyBalAfter"], errors="coerce")
    df["QtyBalBefore"] = pd.to_numeric(df["QtyBalBefore"], errors="coerce")
    df["QtyChange"] = df["QtyBalAfter"] - df["QtyBalBefore"]

    df["Action"] = df["QtyChange"].apply(lambda x: "return" if x > 0 else ("dispense" if x < 0 else "neutral"))
    return df

def get_unreturned_items(df, days):
    df = classify_transactions(df)
    dispenses = df[df["Action"] == "dispense"].copy()
    returns = df[df["Action"] == "return"].copy()

    merged = pd.merge(
        dispenses,
        returns,
        on=["UserName", "ItemTypeName"],
        suffixes=("_disp", "_return")
    )

    merged["DaysBetween"] = (merged["CreatedDate_return"] - merged["CreatedDate_disp"]).dt.days
    merged = merged[merged["DaysBetween"] >= 0]
    valid_returns = merged[merged["DaysBetween"] <= days]

    dispense_ids_with_returns = valid_returns["Id_disp"].unique()
    unreturned_dispenses = dispenses[~dispenses["Id"].isin(dispense_ids_with_returns)]

    cutoff_date = pd.Timestamp.now() - timedelta(days=days)
    unreturned_dispenses = unreturned_dispenses[unreturned_dispenses["CreatedDate"] < cutoff_date]

    return unreturned_dispenses

def create_summary(df, days):
    summary = []
    summary.append(["Analysis Period (days)", days])
    summary.append(["Total Unreturned Items", len(df)])

    type_summary = df.groupby(["ItemTypeName", "ItemSubTypeName"]).size().reset_index(name="Count")
    summary_df = pd.DataFrame(summary, columns=["Description", "Value"])
    return summary_df, type_summary

def autofit_columns(worksheet, df):
    for idx, col in enumerate(df.columns):
        column_len = max(
            df[col].astype(str).map(len).max(),
            len(col)
        ) + 2
        worksheet.set_column(idx, idx, column_len)

def run_app():
    st.title("📦 Unreturned Items Detector")

    uploaded_file = st.file_uploader("Upload Transaction Report (Excel or CSV)", type=["xlsx", "csv"])

    period_option = st.selectbox("Select period for unreturned items:", ["1 week", "1 month", "1 quarter", "Custom"])
    if period_option == "1 week":
        days = 7
    elif period_option == "1 month":
        days = 30
    elif period_option == "1 quarter":
        days = 90
    else:
        days = st.number_input("Enter number of days:", min_value=1, value=30)

    if uploaded_file:
        if uploaded_file.name.endswith("csv"):
            df = pd.read_csv(uploaded_file, dtype=str)
        else:
            df = pd.read_excel(uploaded_file, sheet_name=0, dtype=str)

        column_mapping = {
            "Created Date": "CreatedDate",
            "qty. Bal. Before": "QtyBalBefore",
            "qty. Bal. After": "QtyBalAfter",
            "per. Bal. Before": "PerBalBefore",
            "per. Bal. After": "PerBalAfter",
            "User Full Name": "UserName",
            "Item Type Name": "ItemTypeName",
            "Item Sub Type Name": "ItemSubTypeName",
            "Card ID": "CardId",
            "User ID": "WorkerId",
            "Department Name": "DepartmentName",
            "Title Name": "TitleName",
            "Station Name": "StationName",
            "Transaction Type ID": "TransactionInfoTypeName",
            "From Location": "PreviousLocationName",
            "More Info": "MoreInfo",
            "#": "Id",

            "CreatedDate": "CreatedDate",
            "QtyBalBefore": "QtyBalBefore",
            "QtyBalAfter": "QtyBalAfter",
            "PerBalBefore": "PerBalBefore",
            "PerBalAfter": "PerBalAfter",
            "UserName": "UserName",
            "ItemTypeName": "ItemTypeName",
            "ItemSubTypeName": "ItemSubTypeName",
            "CardId": "CardId",
            "WorkerId": "WorkerId",
            "DepartmentName": "DepartmentName",
            "TitleName": "TitleName",
            "StationName": "StationName",
            "TransactionInfoTypeName": "TransactionInfoTypeName",
            "PreviousLocationName": "PreviousLocationName",
            "Id": "Id"
        }

        df.rename(columns=column_mapping, inplace=True)

        if "CardId" in df.columns:
            df["CardId"] = df["CardId"].apply(lambda x: str(x).strip().split('.')[0] if pd.notna(x) else "")
        if "WorkerId" in df.columns:
            df["WorkerId"] = df["WorkerId"].apply(lambda x: str(x).strip().split('.')[0] if pd.notna(x) else "")

        unreturned = get_unreturned_items(df, days)
        summary_basic, summary_types = create_summary(unreturned, days)

        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            unreturned.to_excel(writer, sheet_name='Unreturned', index=False)
            worksheet1 = writer.sheets['Unreturned']
            autofit_columns(worksheet1, unreturned)

            summary_basic.to_excel(writer, sheet_name='Summary', index=False)
            worksheet2 = writer.sheets['Summary']
            autofit_columns(worksheet2, summary_basic)

            summary_types.to_excel(writer, sheet_name='By Type', index=False)
            worksheet3 = writer.sheets['By Type']
            autofit_columns(worksheet3, summary_types)

        st.success("✅ Report generated with unreturned items and summary.")
        st.download_button(
            label="📥 Download Report",
            data=output.getvalue(),
            file_name="Unreturned_Report.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

if __name__ == "__main__":
    run_app()
