import streamlit as st
import pandas as pd
import io
from datetime import datetime, timedelta


def normalize_columns(df):
    column_map = {
        # Common mappings across xlsx/csv
        "Created Date": "CreatedDate",
        "CreatedDate": "CreatedDate",
        "Card ID": "CardId",
        "CardId": "CardId",
        "RFID Tag": "RFID",
        "RFID": "RFID",
        "Transaction Type ID": "TransactionType",
        "TransactionInfoTypeName": "TransactionType",
        "User Full Name": "UserName",
        "UserName": "UserName",
        "Item Type Name": "ItemTypeName",
        "ItemTypeName": "ItemTypeName",
        "Item Sub Type Name": "ItemSubTypeName",
        "ItemSubTypeName": "ItemSubTypeName"
    }
    df = df.rename(columns={col: column_map.get(col, col) for col in df.columns})
    return df


def get_unreturned_items(df: pd.DataFrame, days: int) -> pd.DataFrame:
    df = normalize_columns(df)
    df["CreatedDate"] = pd.to_datetime(df["CreatedDate"], errors="coerce")
    df = df.dropna(subset=["CreatedDate", "RFID", "TransactionType"])

    latest = df.sort_values("CreatedDate").groupby("RFID", as_index=False).last()
    cutoff = pd.Timestamp.now() - pd.Timedelta(days=days)

    # Treat 'Delivery' as 'Dispense'
    unreturned = latest[
        (latest["TransactionType"].str.lower() == "delivery") &
        (latest["CreatedDate"] < cutoff)
    ]
    return unreturned


def run_app():
    st.title("📦 Unreturned Items Detector")

    uploaded_file = st.file_uploader("Upload Transaction Report (Excel or CSV)", type=["xlsx", "csv"])

    time_options = {
        "1 Week": 7,
        "1 Month": 30,
        "1 Quarter": 90,
        "Custom": None
    }
    option = st.selectbox("Choose timeframe for analysis:", list(time_options.keys()))
    days = time_options[option]
    if option == "Custom":
        days = st.number_input("Enter custom number of days:", min_value=1, max_value=365, value=30)

    if uploaded_file:
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file, dtype=str)
        else:
            df = pd.read_excel(uploaded_file, dtype=str)

        unreturned = get_unreturned_items(df, days)

        summary = unreturned.groupby(["ItemTypeName", "ItemSubTypeName"], dropna=False).size().reset_index(name="Count")
        summary.loc[:, "Analysis Period"] = f"> {days} days"

        output = io.BytesIO()
        with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
            # Save unreturned sheet with selected columns
            cols_to_include = [col for col in [
                "RFID", "CardId", "UserName", "ItemTypeName", "ItemSubTypeName", "CreatedDate", "TransactionType"
            ] if col in unreturned.columns]
            unreturned[cols_to_include].to_excel(writer, sheet_name="Unreturned", index=False)
            summary.to_excel(writer, sheet_name="Summary", index=False)

            # Auto-fit columns
            for sheet_name in writer.sheets:
                worksheet = writer.sheets[sheet_name]
                df_to_use = unreturned[cols_to_include] if sheet_name == "Unreturned" else summary
                for idx, col in enumerate(df_to_use.columns):
                    max_len = max([len(str(x)) for x in df_to_use[col].astype(str).values] + [len(col)]) + 2
                    worksheet.set_column(idx, idx, max_len)

        st.success(f"✅ Found {len(unreturned)} unreturned items older than {days} days.")
        st.download_button(
            label="📥 Download Unreturned Report",
            data=output.getvalue(),
            file_name="Unreturned_Report.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
