
import streamlit as st
import pandas as pd
import io
import re

def normalize_text(s):
    if pd.isna(s):
        return ""
    return re.sub(r"[\u200e\u202c]", "", str(s)).strip()

def run_app():
    st.title("🔍 חיפוש לפי שדה עם מצב גמיש כולל דגם + דיאגנוסטיקה")

    search_mode = st.radio("בחר סוג חיפוש:", ["🔒 חיפוש מדויק", "🔎 חיפוש גמיש (מכיל)"])
    is_exact = search_mode == "🔒 חיפוש מדויק"

    service_file = st.file_uploader("העלה קובץ קריאות שירות", type=["xlsx"])
    parts_file = st.file_uploader("העלה קובץ חלקים", type=["xlsx"])

    if service_file and parts_file:
        service_df = pd.read_excel(service_file)
        parts_df = pd.read_excel(parts_file)

        service_call_col = "מס. קריאה" if "מס. קריאה" in service_df.columns else "מספר קריאה"
        parts_df["מספר קריאה"] = parts_df["מספר קריאה"].astype(str).str.strip().str.replace(".0", "", regex=False)
        service_df[service_call_col] = service_df[service_call_col].astype(str).str.strip().str.replace(".0", "", regex=False)

        merged = pd.merge(
            parts_df,
            service_df[[service_call_col, "תאור תקלה", "תאור קוד פעולה"]],
            left_on="מספר קריאה",
            right_on=service_call_col,
            how="left"
        )

        for col in ["דגם", "תאור תקלה", "תאור קוד פעולה"]:
            merged[col] = merged[col].astype(str).apply(normalize_text).str.strip()

        search_by = st.radio(
            "בחר דרך חיפוש:",
            ["מספר קריאה", "תאור תקלה", "תאור קוד פעולה", "תאור תקלה וגם תאור קוד פעולה"]
        )

        selected_call = selected_fault = selected_action = None
        file_suffix = ""

        if search_by == "מספר קריאה":
            options = merged["מספר קריאה"].dropna().unique()
            selected_call = st.selectbox("בחר מספר קריאה", sorted(options))
            file_suffix = f"מספר_קריאה_{selected_call}"

        elif search_by == "תאור תקלה":
            options = merged["תאור תקלה"].dropna().unique()
            selected_fault = st.selectbox("בחר תאור תקלה", sorted(options))
            file_suffix = f"תאור_תקלה_{selected_fault}"

        elif search_by == "תאור קוד פעולה":
            options = merged["תאור קוד פעולה"].dropna().unique()
            selected_action = st.selectbox("בחר תאור קוד פעולה", sorted(options))
            file_suffix = f"תאור_פעולה_{selected_action}"

        elif search_by == "תאור תקלה וגם תאור קוד פעולה":
            faults = merged["תאור תקלה"].dropna().unique()
            selected_fault = st.selectbox("בחר תאור תקלה", sorted(faults), key="fault_combo")

            selected_action = None
            if selected_fault:
                filtered_actions = merged[merged["תאור תקלה"] == selected_fault]["תאור קוד פעולה"].dropna().unique()
                selected_action = st.selectbox("בחר תאור קוד פעולה", sorted(filtered_actions), key="action_combo")
                file_suffix = f"תקלה_{selected_fault}_פעולה_{selected_action}"

        if st.button("🔍 חפש"):
            if search_by == "מספר קריאה" and selected_call:
                filtered = merged[merged["מספר קריאה"] == selected_call]

            elif search_by == "תאור תקלה" and selected_fault:
                filtered = merged[
                    merged["תאור תקלה"].str.contains(selected_fault, na=False)
                ] if not is_exact else merged[merged["תאור תקלה"] == selected_fault]

            elif search_by == "תאור קוד פעולה" and selected_action:
                filtered = merged[
                    merged["תאור קוד פעולה"].str.contains(selected_action, na=False)
                ] if not is_exact else merged[merged["תאור קוד פעולה"] == selected_action]

            elif search_by == "תאור תקלה וגם תאור קוד פעולה" and selected_fault and selected_action:
                if is_exact:
                    filtered = merged[
                        (merged["תאור תקלה"] == selected_fault) &
                        (merged["תאור קוד פעולה"] == selected_action) &
                        (merged["דגם"] == "DX00 PRO")
                    ]
                else:
                    filtered = merged[
                        merged["תאור תקלה"].str.contains(selected_fault, na=False) &
                        merged["תאור קוד פעולה"].str.contains(selected_action, na=False) &
                        merged["דגם"].str.contains("DX00", na=False)
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
                    worksheet = writer.sheets['תוצאות חיפוש']
                    for i, col in enumerate(filtered_result.columns):
                        max_len = max(filtered_result[col].astype(str).map(len).max(), len(col)) + 1
                        worksheet.set_column(i, i, max_len)

                output.seek(0)
                safe_suffix = file_suffix.replace(" ", "_").replace("/", "_")
                st.download_button(
                    label="📥 הורד תוצאות לאקסל",
                    data=output,
                    file_name=f"תוצאות_חיפוש_{safe_suffix}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
            else:
                st.warning("לא נמצאו תוצאות.")

        # Diagnostic
        if search_by == "תאור תקלה וגם תאור קוד פעולה" and selected_fault and selected_action and st.checkbox("הצג דיאגנוסטיקה לשורות שלא נמצאו"):
            diagnostic = merged[merged["תאור תקלה"].notna() & merged["תאור קוד פעולה"].notna()].copy()
            diagnostic["✅ דגם תואם"] = diagnostic["דגם"].str.contains("DX00", na=False)
            diagnostic["✅ תקלה תואמת"] = diagnostic["תאור תקלה"].str.contains(selected_fault, na=False)
            diagnostic["✅ פעולה תואמת"] = diagnostic["תאור קוד פעולה"].str.contains(selected_action, na=False)
            diagnostic["📌 סיבה"] = diagnostic.apply(
                lambda row: "❌ דגם" if not row["✅ דגם תואם"]
                else "❌ תקלה" if not row["✅ תקלה תואמת"]
                else "❌ פעולה" if not row["✅ פעולה תואמת"]
                else "✔️ תואם", axis=1
            )
            st.dataframe(diagnostic[["מספר קריאה", "דגם", "תאור תקלה", "תאור קוד פעולה", "📌 סיבה"]])
