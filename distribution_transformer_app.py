import streamlit as st
import pandas as pd
import io
import re

# ⚠️ DO NOT set page config inside this function if you're importing it in another Streamlit app
# Move this to the main app file if this will be part of a larger toolkit

def run_transformer_app():
    st.title("📂 Service Distribution Transformer")
    st.markdown("Upload an Excel file and get an updated version with normalized \"מק\"ט\" and \"תאור\" values.")

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

    uploaded_file = st.file_uploader("Upload Excel File", type=["xlsx"])

    if uploaded_file is not None:
        try:
            df = pd.read_excel(uploaded_file)

            if 'מק"ט' not in df.columns:
                st.error("The file must contain a column named 'מק\"ט'.")
            else:
                df[['מק"ט', 'תאור']] = df.apply(lambda row: pd.Series(transform_row(row['מק"ט'])), axis=1)
                st.subheader("Updated Preview")
                st.dataframe(df.head(20))

                output = io.BytesIO()
                df.to_excel(output, index=False)
                output.seek(0)

                st.download_button("📥 Download Updated Excel",
                                   data=output,
                                   file_name="Updated_Distribution_Data.xlsx",
                                   mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

        except Exception as e:
            st.error(f"Error processing file: {e}")
    else:
        st.info("Awaiting Excel file upload...")
