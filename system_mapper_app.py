import streamlit as st
import pandas as pd
import re
from io import BytesIO

st.set_page_config(page_title="System Mapper", layout="centered")
st.title("🧭 System Model Mapper for Polytex Reports")

# Logic for mapping models
def transform_row(makat: str):
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

# Try all column name candidates
column_candidates = ['מק"ט', 'מק"ט בטיפול', "מק'ט"]
desc_candidates = ['תאור מוצר', 'תאור מוצר בטיפול']


uploaded_files = st.file_uploader("📁 Upload one or more Excel reports", type=["xlsx"], accept_multiple_files=True)

if uploaded_files:
    for file in uploaded_files:
        try:
            df = pd.read_excel(file)

            makat_col = next((col for col in column_candidates if col in df.columns), None)
            desc_col = next((col for col in desc_candidates if col in df.columns), None)

            if not makat_col or not desc_col:
                st.warning(f"⚠️ Required columns not found in {file.name}. Skipping.")
                continue

            df[[makat_col, desc_col]] = df[makat_col].apply(lambda x: pd.Series(transform_row(x)))

            # Save back to Excel
            output = BytesIO()
            with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
                df.to_excel(writer, sheet_name="DataSheet", index=False)
            output.seek(0)

            st.download_button(
                label=f"📥 Download Mapped Report: {file.name}",
                data=output,
                file_name=f"{file.name.replace('.xlsx', '_mapped.xlsx')}",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

        except Exception as e:
            st.error(f"❌ Failed to process {file.name}: {e}")
