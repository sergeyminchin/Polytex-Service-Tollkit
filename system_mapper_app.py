
import streamlit as st
import pandas as pd
import re
from io import BytesIO

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
    st.title("🧠 System Mapper")
    uploaded_files = st.file_uploader("Upload Excel File(s)", type=["xlsx"], accept_multiple_files=True)

    if uploaded_files:
        for file in uploaded_files:
            try:
                df = pd.read_excel(file)
                column_candidates = ["מק"ט", "מק"ט בטיפול", "מק'ט"]

                matched_col = next((col for col in column_candidates if col in df.columns), None)

                if not matched_col:
                    st.warning(f"⚠️ No matching column found in: {file.name}")
                    continue

                df[matched_col], df["תאור מוצר"] = zip(*df[matched_col].map(transform_row))

                output = BytesIO()
                with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
                    df.to_excel(writer, index=False, sheet_name="DataSheet")
                output.seek(0)

                st.success(f"✅ Processed file: {file.name}")
                st.download_button(
                    label=f"📥 Download {file.name}",
                    data=output,
                    file_name=f"{Path(file.name).stem}_mapped.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
            except Exception as e:
                st.error(f"❌ Error processing {file.name}: {e}")
