
import streamlit as st
import pandas as pd
import io
import re

def normalize_text(s):
    if pd.isna(s):
        return ""
    return re.sub(r"[\u200e\u202c]", "", str(s)).strip()

def run_app():
    st.title("🔍 חיפוש לפי שדה כולל קריאות ללא חלקים")

    search_mode = st.radio("בחר סוג חיפוש:", ["🔒 חיפוש מדויק", "🔎 חיפוש גמיש (מכיל)"])
    is_exact = search_mode == "🔒 חיפוש מדויק"

    service_file = st.file_uploader("העלה קובץ קריאות שירות", type=["xlsx"])
    parts_file = st.file_uploader("העלה קובץ חלקים", type=["xlsx"])

    if service_file and parts_file:
        service_df = pd.read_excel(service_file)
        parts_df = pd.read_excel(parts_file)

        call_col = "מס. קריאה" if "מס. קריאה" in service_df.columns else "מספר קריאה"
        parts_df["מספר קריאה"] = parts_df["מספר קריאה"].astype(str).str.strip().str.replace(".0", "", regex=False)
        service_df[call_col] = service_df[call_col].astype(str).str.strip().str.replace(".0", "", regex=False)

        merged = pd.merge(service_df, parts_df, left_on=call_col, right_on="מספר קריאה", how="left")

        if "דגם_x" in merged.columns:
            merged.rename(columns={"דגם_x": "דגם"}, inplace=True)

        for col in ["דגם", "תאור תקלה", "תאור קוד פעולה"]:
            if col in merged.columns:
                merged[col] = merged[col].astype(str).apply(normalize_text).str.strip()

        search_by = st.radio(
            "בחר דרך חיפוש:",
            ["מספר קריאה", "תאור תקלה", "תאור קוד פעולה", "תאור תקלה וגם תאור קוד פעולה"]
        )

        selected_call = selected_fault = selected_action = None
        file_suffix = ""

        if search_by == "מספר קריאה":
            options = merged[call_col].dropna().unique()
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

            if selected_fault:
                actions = merged[merged["תאור תקלה"] == selected_fault]["תאור קוד פעולה"].dropna().unique()
                selected_action = st.selectbox("בחר תאור קוד פעולה", sorted(actions), key="action_combo")
                file_suffix = f"תקלה_{selected_fault}_פעולה_{selected_action}"

        if st.button("🔍 חפש"):
            if search_by == "מספר קריאה" and selected_call:
                filtered = merged[merged[call_col] == selected_call]
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
                        (merged["תאור קוד פעולה"] == selected_action)
                    ]
                else:
                    filtered = merged[
                        merged["תאור תקלה"].str.contains(selected_fault, na=False) &
                        merged["תאור קוד פעולה"].str.contains(selected_action, na=False)
                    ]
            else:
                filtered = pd.DataFrame()

            if not filtered.empty:
                display_cols = [
                    call_col, "דגם", "תאור תקלה", "תאור קוד פעולה",
                    'מק"ט - חלק', "תאור מוצר - חלק", "כמות בפועל"
                ]
                available_cols = [col for col in display_cols if col in filtered.columns]
                final_result = filtered[available_cols].drop_duplicates()

                st.dataframe(final_result)

                output = io.BytesIO()
                with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
                    final_result.to_excel(writer, index=False, sheet_name="תוצאות חיפוש")
                    sheet = writer.sheets["תוצאות חיפוש"]
                    for i, col in enumerate(final_result.columns):
                        width = max(final_result[col].astype(str).map(len).max(), len(col)) + 1
                        sheet.set_column(i, i, width)

                output.seek(0)
                st.download_button(
                    label="📥 הורד תוצאות לאקסל",
                    data=output,
                    file_name=f"תוצאות_חיפוש_{file_suffix.replace(' ', '_')}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
            else:
                st.warning("לא נמצאו תוצאות.")
