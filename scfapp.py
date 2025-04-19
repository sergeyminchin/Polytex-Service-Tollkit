
import streamlit as st
import pandas as pd
import io

def run_app():
    st.title("🔍 חיפוש לפי שדה עם אפשרויות מתוך הקובץ")

    service_file = st.file_uploader("העלה קובץ קריאות שירות", type=["xlsx"])
    parts_file = st.file_uploader("העלה קובץ חלקים", type=["xlsx"])

    if service_file and parts_file:
        try:
            service_df = pd.read_excel(service_file)
            parts_df = pd.read_excel(parts_file)
        except Exception as e:
            st.error(f"שגיאה בטעינת הקבצים: {e}")
            return

        service_call_col = "מס. קריאה" if "מס. קריאה" in service_df.columns else "מספר קריאה"
        merged = pd.merge(
            parts_df,
            service_df[[service_call_col, "תאור תקלה", "תאור קוד פעולה"]],
            left_on="מספר קריאה",
            right_on=service_call_col,
            how="left"
        )

        search_mode = st.radio(
            "בחר דרך חיפוש:",
            ["מספר קריאה", "תאור תקלה", "תאור קוד פעולה", "תאור תקלה וגם תאור קוד פעולה"]
        )

        selected_call = selected_fault = selected_action = None

        if search_mode == "מספר קריאה":
            options = merged["מספר קריאה"].astype(str).dropna().unique()
            selected_call = st.selectbox("בחר מספר קריאה", sorted(options))
        elif search_mode == "תאור תקלה":
            options = merged["תאור תקלה"].dropna().unique()
            selected_fault = st.selectbox("בחר תאור תקלה", sorted(options))
        elif search_mode == "תאור קוד פעולה":
            options = merged["תאור קוד פעולה"].dropna().unique()
            selected_action = st.selectbox("בחר תאור קוד פעולה", sorted(options))
        elif search_mode == "תאור תקלה וגם תאור קוד פעולה":
            faults = merged["תאור תקלה"].dropna().unique()
            actions = merged["תאור קוד פעולה"].dropna().unique()
            selected_fault = st.selectbox("בחר תאור תקלה", sorted(faults), key="fault_combo")
            selected_action = st.selectbox("בחר תאור קוד פעולה", sorted(actions), key="action_combo")

        if st.button("🔍 חפש"):
            if search_mode == "מספר קריאה" and selected_call:
                filtered = merged[merged["מספר קריאה"].astype(str) == str(selected_call)]
            elif search_mode == "תאור תקלה" and selected_fault:
                filtered = merged[merged["תאור תקלה"] == selected_fault]
            elif search_mode == "תאור קוד פעולה" and selected_action:
                filtered = merged[merged["תאור קוד פעולה"] == selected_action]
            elif search_mode == "תאור תקלה וגם תאור קוד פעולה" and selected_fault and selected_action:
                filtered = merged[
                    (merged["תאור תקלה"] == selected_fault) &
                    (merged["תאור קוד פעולה"] == selected_action)
                ]
            else:
                filtered = pd.DataFrame()

            if not filtered.empty:
                display_cols = [
                    "מספר קריאה", "דגם", "תאור תקלה", "תאור קוד פעולה",
                    'מק"ט - חלק', "תאור מוצר - חלק", "כמות בפועל"
                ]
                existing_cols = [col for col in display_cols if col in filtered.columns]
                filtered_result = filtered[existing_cols].drop_duplicates()

                st.dataframe(filtered_result)

                output = io.BytesIO()
                with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                    filtered_result.to_excel(writer, index=False, sheet_name='תוצאות חיפוש')
                output.seek(0)

                st.download_button(
                    label="📥 הורד תוצאות לאקסל",
                    data=output,
                    file_name="תוצאות_חיפוש.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
            else:
                st.warning("לא נמצאו תוצאות.")
