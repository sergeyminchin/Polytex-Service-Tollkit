import streamlit as st
import pandas as pd
import re
from io import BytesIO
from PIL import Image

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

def run_app():
    st.title("🧩 System Mapper")

    uploaded_files = st.file_uploader("📤 Upload up to 3 Excel files", type=["xlsx"], accept_multiple_files=True)

    if uploaded_files:
        for uploaded_file in uploaded_files:
            try:
                df = pd.read_excel(uploaded_file)
                col_name = next((col for col in df.columns if col in ["מק"ט", "מק"ט בטיפול", "מק'ט"]), None)
                desc_col = next((col for col in df.columns if "תאור" in col and "מוצר" in col), None)

                if not col_name or not desc_col:
                    st.warning(f"⚠️ Skipped {uploaded_file.name} (No valid מק"ט column found).")
                    continue

                mapped = df[col_name].apply(lambda x: transform_row(x))
                df[col_name], df[desc_col] = zip(*mapped)

                output = BytesIO()
                with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
                    df.to_excel(writer, sheet_name="DataSheet", index=False)
                output.seek(0)

                st.download_button(
                    label=f"📥 Download: {uploaded_file.name}",
                    data=output,
                    file_name=uploaded_file.name,
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
            except Exception as e:
                st.error(f"❌ Failed to process {uploaded_file.name}: {e}")
