
import streamlit as st
import pandas as pd
from io import BytesIO

def map_system(row):
    part_code = str(row.get("מק"ט", "")).upper()
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
        return row["מק"ט"], row["תאור"]

def run_transformer_app():
    st.title("📦 Distribution Transformer Analyzer")

    uploaded_file = st.file_uploader("Upload Distribution Fixes Excel File", type=["xlsx"])

    if uploaded_file:
        try:
            df = pd.read_excel(uploaded_file)
        except Exception as e:
            st.error(f"❌ Failed to read Excel file: {e}")
            return

        if "מק"ט" not in df.columns or "תאור" not in df.columns:
            st.error("❌ The file must contain the columns: 'מק"ט' and 'תאור'")
            return

        # Apply system mapping logic
        df[["מק"ט", "תאור"]] = df.apply(map_system, axis=1, result_type="expand")
        
        st.success("✅ Mapping applied successfully. Preview below:")
        st.dataframe(df.head(20))

        output = BytesIO()
        df.to_excel(output, index=False)
        st.download_button("📥 Download Transformed Excel", data=output.getvalue(),
                           file_name="transformed_distribution_fixes.xlsx",
                           mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
