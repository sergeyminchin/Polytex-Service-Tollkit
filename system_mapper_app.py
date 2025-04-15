
import streamlit as st
import pandas as pd
import re
from io import BytesIO

st.set_page_config(page_title="System Mapper", layout="centered")

def transform_row(makat):
    makat = str(makat).upper()
    if makat in ["POL-R11I-00000A"]:
        return "R110", "R110 Return Unit"
    elif makat in ["POL-A-D200", "PO-POL-A-D200/F"]:
        return "DX00", "DX00 Distribution Cabinet"
    elif re.search(r"(200P|300P|PRO)", makat):
        return "DX00 PRO", "DX00 PRO Distribution Cabinet"
    elif re.search(r"(D200|D300)", makat) and not re.search(r"(PRO|P)", makat):
        return "DX00", "DX00 Distribution Cabinet"
    elif re.search(r"(D10|D12|D16|D20|D24|D40)", makat):
        return "DXX", "DXX Distribution Cabinet"
    elif re.search(r"(310P|31XP)", makat):
        return "R310 PRO", "R310 PRO Return Unit"
    elif re.search(r"(R31X|R310|R300)", makat) and not re.search(r"(PRO|P)", makat):
        return "R310", "R310 Return Unit"
    elif re.search(r"(R11X|R110|R100)", makat) and not re.search(r"(PRO|P)", makat):
        return "R110", "R110 Return Unit"
    else:
        return makat, ""

def run_app():
    st.title("🧠 System Mapper Utility")
    uploaded_files = st.file_uploader("Upload 1–3 Excel Files", type=["xlsx"], accept_multiple_files=True)

    if uploaded_files:
        for file in uploaded_files:
            try:
                df = pd.read_excel(file)
                makat_column = next((col for col in df.columns if any(key in col for key in ["מק"ט", "מק'", "מקט"])), None)
                desc_column = next((col for col in df.columns if "תיאור" in col and "מוצר" in col), None)

                if not makat_column:
                    st.error(f"No valid 'makat' column in {file.name}. Skipping.")
                    continue

                df[makat_column], df[desc_column] = zip(*df[makat_column].map(transform_row))
                output = BytesIO()
                with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
                    df.to_excel(writer, sheet_name="DataSheet", index=False)
                st.download_button(f"📥 Download: {file.name}", data=output.getvalue(), file_name=file.name, mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
            except Exception as e:
                st.error(f"❌ Failed to process {file.name}: {e}")
