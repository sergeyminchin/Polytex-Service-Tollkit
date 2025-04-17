import streamlit as st
import pandas as pd
import io

def run_app():
    st.title("🔧 חיפוש לפי קריאת שירות או תיאור תקלה / פעולה")

    service_file = st.file_uploader("העלה קובץ קריאות שירות", type=["xlsx"])
    parts_file = st.file_uploader("העלה קובץ חלקים", type=["xlsx"])

    if "last_search_by" not in st.session_state:
        st.session_state.last_search_by = "מספר קריאה"
    if "query" not in st.session_state:
        st.session_state.query = ""
    if "query_fault" not in st.session_state:
        st.session_state.query_fault = ""
    if "query_action" not in st.session_state:
        st.session_state.query_action = ""
    if "search_triggered" not in st.session_state:
        st.session_state.search_triggered = False

    if service_file and parts_file:
        try:
            service_df = pd.read_excel(service_file)
            parts_df = pd.read_excel(parts_file)
        except Exception as e:
            st.error(f"שגיאה בטעינת הקבצים: {e}")
        else:
            service_call_col = "מס. קריאה" if "מס. קריאה" in service_df.columns else "מספר קריאה"
            merged = pd.merge(
                parts_df,
                service_df[[service_call_col, "תאור תקלה", "תאור קוד פעולה"]],
                left_on="מספר קריאה",
                right_on=service_call_col,
                how="left"
            )

            search_by = st.radio(
                "בחר דרך חיפוש:",
                ["מספר קריאה", "תאור תקלה", "תאור קוד פעולה", "תאור תקלה וגם תאור קוד פעולה"]
            )

            if search_by != st.session_state.last_search_by:
                st.session_state.query = ""
                st.session_state.query_fault = ""
                st.session_state.query_action = ""
                st.session_state.search_triggered = False
            st.session_state.last_search_by = search_by

            if search_by == "תאור תקלה וגם תאור קוד פעולה":
                query_fault = st.text_input("תאור תקלה", value=st.session_state.query_fault)
                query_action = st.text_input("תאור קוד פעולה", value=st.session_state.query_action)
                st.session_state.query_fault = query_fault
                st.session_state.query_action = query_action
            else:
                query = st.text_input("הזן את הערך לחיפוש", value=st.session_state.query)
                st.session_state.query = query

            if st.button("🔍 חפש"):
                st.session_state.search_triggered = True

            if st.session_state.search_triggered:
                if search_by == "מספר קריאה" and st.session_state.query:
                    filtered = merged[merged["מספר קריאה"].astype(str).str.contains(st.session_state.query)]
                elif search_by == "תאור תקלה" and st.session_state.query:
                    filtered = merged[merged["תאור תקלה"].astype(str).str.contains(st.session_state.query, case=False, na=False)]
                elif search_by == "תאור קוד פעולה" and st.session_state.query:
                    filtered = merged[merged["תאור קוד פעולה"].astype(str).str.contains(st.session_state.query, case=False, na=False)]
                elif search_by == "תאור תקלה וגם תאור קוד פעולה" and (st.session_state.query_fault and st.session_state.query_action):
                    filtered = merged[
                        merged["תאור תקלה"].astype(str).str.contains(st.session_state.query_fault, case=False, na=False) &
                        merged["תאור קוד פעולה"].astype(str).str.contains(st.session_state.query_action, case=False, na=False)
                    ]
                else:
                    filtered = pd.DataFrame()

                if not filtered.empty:
                    display_cols = [
                        "מספר קריאה", "דגם", "תאור תקלה", "תאור קוד פעולה",
                        "מק\"ט - חלק", "תאור מוצר - חלק", "כמות בפועל"
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
