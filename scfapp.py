
import streamlit as st
import pandas as pd
import io

def run_app():
    st.title("🔍 חיפוש דינמי לפי שדות בקובץ")

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

        # הצגת עמודות טקסטואליות לחיפוש
        search_fields = [col for col in merged.columns if merged[col].dtype == "object" or merged[col].dtype.name == "string"]
        selected_fields = st.multiselect("בחר שדות לחיפוש:", search_fields, default=["מספר קריאה"])

        user_queries = {}
        for field in selected_fields:
            user_queries[field] = st.text_input(f"הזן ערך לחיפוש ב־{field}", key=f"query_{field}")

        if st.button("🔍 חפש"):
            filtered = merged.copy()
            for field, query in user_queries.items():
                if query:
                    query_clean = str(query).strip()
                    filtered[field] = filtered[field].astype(str).str.strip()
                    filtered = filtered[filtered[field].str.contains(query_clean, case=False, na=False)]

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
