import streamlit as st
import pandas as pd
import io
from datetime import datetime, timedelta


def get_unreturned_items(df: pd.DataFrame, days: int) -> pd.DataFrame:
    df = df.copy()
    df["CreatedDate"] = pd.to_datetime(df["CreatedDate"], errors="coerce")
    df = df.dropna(subset=["CardId", "CreatedDate", "TransactionInfoTypeName"])

    # Get the last transaction per CardId (RFID)
    latest = df.sort_values("CreatedDate").groupby("CardId", as_index=False).last()
    cutoff = pd.Timestamp.now() - pd.Timedelta(days=days)

    # Only those still marked Dispensed and older than cutoff
    unreturned = latest[
        (latest["TransactionInfoTypeName"].str.lower() == "dispensed") &
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

        summary = unreturned.groupby(["ItemTypeName", "ItemSubTypeName"]).size().reset_index(name="Count")
        summary_sheet = summary.copy()
        summary_sheet.loc[:, "Analysis Period"] = f"> {days} days"

        output = io.BytesIO()
        with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
            unreturned.to_excel(writer, sheet_name="Unreturned", index=False)
            summary_sheet.to_excel(writer, sheet_name="Summary", index=False)

            # Auto-fit column widths
            for sheet in writer.sheets.values():
                worksheet = sheet
                for idx, col in enumerate(unreturned.columns):
                    max_len = max(
                        [len(str(val)) for val in unreturned[col].values] + [len(col)]
                    ) + 1
                    worksheet.set_column(idx, idx, max_len)

        st.success(f"✅ Found {len(unreturned)} unreturned items older than {days} days.")
        st.download_button(
            label="📥 Download Unreturned Report",
            data=output.getvalue(),
            file_name="Unreturned_Report.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
