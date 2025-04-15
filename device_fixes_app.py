import streamlit as st
import pandas as pd
from io import BytesIO

st.title("🔧 Device Fixes Analyzer")
uploaded_file = st.file_uploader("Upload your Excel file (must include a 'DataSheet' tab & מק"ט column)", type=["xlsx"])
if uploaded_file:
    df = pd.read_excel(uploaded_file, sheet_name='DataSheet')
    df = df.sort_values(by=["מס' מכשיר", "תאריך קריאה"])
    df["Previous Call Date"] = df.groupby("מס' מכשיר")["תאריך קריאה"].shift(1)
    df["Days Since Last Call"] = (df["תאריך קריאה"] - df["Previous Call Date"]).dt.days
    df["Repeated Call"] = df["Days Since Last Call"] <= 30
    st.success("File loaded successfully!")

    st.header("📅 Filter Options")
    min_date = df["תאריך קריאה"].min()
    max_date = df["תאריך קריאה"].max()
    date_range = st.date_input("Select date range", [min_date, max_date])
    filtered_df = df[(df["תאריך קריאה"] >= pd.to_datetime(date_range[0])) & (df["תאריך קריאה"] <= pd.to_datetime(date_range[1]))]

    st.markdown(f"📌 **Total service calls in range:** {len(filtered_df)}")

    st.header("✅ Select Analyses to Run")
    run_unique = st.checkbox("How many unique devices were fixed")
    run_common_faults = st.checkbox("Most common problem descriptions")
    run_model_calls = st.checkbox("Number of calls per model code")
    run_problem_device = st.checkbox("Most problematic device (by device number)")
    run_problem_product = st.checkbox("Most problematic product (by description)")
    run_repeat_stats = st.checkbox("Repeated call analysis")
    run_tech_stats = st.checkbox("Technician workload and repeated calls")
    run_device_lifecycle = st.checkbox("Device lifecycle analysis")
    run_faults_by_product = st.checkbox("Most common faults by product")
    run_device_excel = st.checkbox("🔄 Export separate Excel file: per device")
    run_tech_excel = st.checkbox("🔄 Export separate Excel file: per technician")

    if "outputs" not in st.session_state:
        st.session_state["outputs"] = {}

    if st.button("Run Analysis"):
        output_main = BytesIO()
        output_devices = BytesIO()
        output_techs = BytesIO()
        repeated = filtered_df[filtered_df["Repeated Call"] == True]

        with pd.ExcelWriter(output_main, engine="xlsxwriter") as writer:
            if run_unique:
                unique_devices = filtered_df["מס' מכשיר"].nunique()
                pd.DataFrame([{"Unique Devices Fixed": unique_devices}]).to_excel(writer, sheet_name="Unique Devices", index=False)

            if run_common_faults:
                fault_counts = filtered_df["תאור קוד התקלה"].value_counts().reset_index()
                fault_counts.columns = ["Problem", "Count"]
                fault_counts.to_excel(writer, sheet_name="Common Faults", index=False)

            if run_model_calls:
                model_counts = filtered_df["מק'ט"].value_counts().reset_index()
                model_counts.columns = ["Model Code", "Number of Calls"]
                model_counts.to_excel(writer, sheet_name="Model Call Counts", index=False)

            if run_problem_device:
                device_counts = filtered_df["מס' מכשיר"].value_counts().reset_index()
                device_counts.columns = ["Device Number", "Number of Calls"]
                top_device = device_counts.iloc[0]["Device Number"]
                top_device_data = filtered_df[filtered_df["מס' מכשיר"] == top_device][["תאריך קריאה", "תאור קוד התקלה", "תאור התיקון"]]
                device_counts.to_excel(writer, sheet_name="Most Problematic Device", index=False)
                top_device_data.to_excel(writer, sheet_name=f"Device {top_device}", index=False)

            if run_problem_product:
                product_counts = filtered_df["תאור מוצר"].value_counts().reset_index()
                product_counts.columns = ["Product Description", "Number of Calls"]
                product_counts.to_excel(writer, sheet_name="Most Problematic Product", index=False)

            if run_repeat_stats:
                repeated_problems = (
                    repeated.groupby(["תאור מוצר", "תאור קוד התקלה"])
                    .size()
                    .reset_index(name="Repeated Call Count")
                    .sort_values(by="Repeated Call Count", ascending=False)
                )
                repeated_problems.to_excel(writer, sheet_name="Repeated Problems", index=False)

            if run_tech_stats:
                tech_calls = filtered_df["שם טכנאי"].value_counts().reset_index()
                tech_calls.columns = ["Technician", "Number of Calls"]
                repeated_tech = repeated["שם טכנאי"].value_counts().reset_index()
                repeated_tech.columns = ["Technician", "Repeated Calls"]
                tech_stats = pd.merge(tech_calls, repeated_tech, on="Technician", how="left").fillna(0)
                tech_stats["Repeated Calls"] = tech_stats["Repeated Calls"].astype(int)
                tech_stats["% Repeated"] = round((tech_stats["Repeated Calls"] / tech_stats["Number of Calls"]) * 100, 2)
                tech_stats.to_excel(writer, sheet_name="Technician Stats", index=False)

            if run_device_lifecycle:
                repairs_per_device = filtered_df.groupby("מס' מכשיר").size().reset_index(name="Total Repairs")
                dates = filtered_df.groupby("מס' מכשיר")["תאריך קריאה"].agg(["min", "max"]).reset_index()
                dates.columns = ["מס' מכשיר", "First Repair", "Last Repair"]
                lifecycle = pd.merge(repairs_per_device, dates, on="מס' מכשיר")
                lifecycle = lifecycle[lifecycle["Total Repairs"] > 1]
                lifecycle["Lifecycle (Days)"] = (lifecycle["Last Repair"] - lifecycle["First Repair"]).dt.days
                lifecycle.to_excel(writer, sheet_name="Device Lifecycle", index=False)

            if run_faults_by_product:
                faults_by_product = (
                    filtered_df.groupby(["תאור מוצר", "תאור קוד התקלה"])
                    .size()
                    .reset_index(name="Fault Count")
                    .sort_values(["תאור מוצר", "Fault Count"], ascending=[True, False])
                )
                faults_by_product.to_excel(writer, sheet_name="Faults by Product", index=False)

        if run_device_excel:
            with pd.ExcelWriter(output_devices, engine="xlsxwriter") as writer:
                for device_number, group in filtered_df.groupby("מס' מכשיר"):
                    sheet_name = str(device_number)[:31]
                    group.to_excel(writer, sheet_name=sheet_name, index=False)

        if run_tech_excel:
            with pd.ExcelWriter(output_techs, engine="xlsxwriter") as writer:
                for tech_name, group in filtered_df.groupby("שם טכנאי"):
                    sheet_name = str(tech_name)[:31].replace("/", "_").replace("\\", "_")
                    group.to_excel(writer, sheet_name=sheet_name, index=False)

        st.session_state.outputs["main"] = output_main.getvalue()
        st.session_state.outputs["devices"] = output_devices.getvalue() if run_device_excel else None
        st.session_state.outputs["techs"] = output_techs.getvalue() if run_tech_excel else None
        st.session_state["download_ready"] = True

    if st.session_state.get("download_ready"):
        st.success("✅ Files are ready for download:")
        st.download_button("📥 Download Main Excel Report", st.session_state.outputs["main"], "device_analysis_results.xlsx")
        if st.session_state.outputs["devices"]:
            st.download_button("📥 Download Per-Device File", st.session_state.outputs["devices"], "per_device.xlsx")
        if st.session_state.outputs["techs"]:
            st.download_button("📥 Download Per-Technician File", st.session_state.outputs["techs"], "per_technician.xlsx")
