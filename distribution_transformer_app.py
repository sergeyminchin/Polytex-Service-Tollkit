
import streamlit as st
import pandas as pd
from io import BytesIO
from PIL import Image

def map_model(part_code):
    part_code = str(part_code).upper()
    if any(x in part_code for x in ["D200", "D300"]) and not any(x in part_code for x in ["PRO", "P"]):
        return "DX00", "DX00 Distribution Cabinet"
    elif any(x in part_code for x in ["200P", "300P", "PRO"]):
        return "DX00 PRO", "DX00 PRO Distribution Cabinet"
    elif any(x in part_code for x in ["R31X", "R310", "R300", "R310X"]) and not any(x in part_code for x in ["PRO", "P"]):
        return "R310", "R310 Return Unit"
    elif any(x in part_code for x in ["R11X", "R110", "R100", "R110X"]) and not any(x in part_code for x in ["PRO", "P"]):
        return "R110", "R110 Return Unit"
    elif any(x in part_code for x in ["310P", "31XP"]):
        return "R310 PRO", "R310 PRO Return Unit"
    elif part_code == "PO-POL-A-D200/F":
        return "DX00", "DX00 Distribution Cabinet"
    elif part_code == "POL-A-D200":
        return "DX00", "DX00 Distribution Cabinet"
    elif part_code == "POL-R11I-00000A":
        return "R110", "R110 Return Unit"
    else:
        return part_code, part_code

def run_transformer_app():
    st.title("📦 Service Distribution Transformer")

    uploaded_file = st.file_uploader("Upload Excel File", type=["xlsx"])
    if uploaded_file:
        try:
            df = pd.read_excel(uploaded_file)
            df["מק"ט"], df["תאור מוצר"] = zip(*df["מק"ט"].map(map_model))
            counts = df.groupby(["מק"ט", "תאור מוצר"]).size().reset_index(name="כמות")
            
            st.dataframe(counts)

            output = BytesIO()
            with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
                counts.to_excel(writer, index=False, sheet_name="Analysis")
            output.seek(0)

            st.download_button(
                label="📥 Download Excel File",
                data=output,
                file_name="distribution_transformer_analysis.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        except Exception as e:
            st.error(f"❌ Failed to process file: {e}")
