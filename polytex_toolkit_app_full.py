# 🔁 Ensure missing tools in config also exist in app_options
default_missing_tools = {
    "🫲 Alerts Filtering": "alerts_analyzer_streamlit",
    "🔗 Helpful Links": "helpful_links"
}
for tool_name, tool_file in default_missing_tools.items():
    if tool_name not in app_options:
        app_options[tool_name] = tool_file
    if tool_name not in st.session_state.tool_config:
        st.session_state.tool_config[tool_name] = {"visible": True, "order": len(st.session_state.tool_config)}
if "🔗 Helpful Links" not in st.session_state.tool_config:
    st.session_state.tool_config["🔗 Helpful Links"] = {"visible": True, "order": 14}

visible_tools = {
    tool: app_options[tool]
    for tool, settings in sorted(st.session_state.tool_config.items(), key=lambda x: x[1]["order"])
    if settings["visible"]
}

if not visible_tools:
    st.warning("No tools enabled. Enable at least one in Admin panel.")
    st.stop()

selected_tool = st.selectbox("Select a Tool", list(visible_tools.keys()))
app_file = visible_tools[selected_tool]

# ===============================
# ▶️ Tool Loader
# ===============================
if app_file == "repeated_calls":
    import repeated_calls
    repeated_calls.run_app()
elif app_file == "distribution_transformer_app":
    from distribution_transformer_app import run_transformer_app
    run_transformer_app()
elif app_file == "parts_dashboard":
    import parts_dashboard
    parts_dashboard.run_app()
elif app_file == "system_mapper_app_final":
    import system_mapper_app_final as system_mapper_app
    system_mapper_app.run_app()
elif app_file == "help_app":
    import help_app
    help_app.run_app()
elif app_file == "ugs":
    import ugs
    ugs.run_app()
elif app_file == "scfapp":
    import scfapp
    scfapp.run_app()
elif app_file == "nri":
    import nri
    nri.run_app()
elif app_file == "helpful_links":
    st.subheader("🔗 Helpful Links")
    st.markdown("Here are some useful resources for the service team:")
    st.markdown("""
    - [🌐 Polytex Manager (PM8)](https://pm8.polytex.cloud/)
    - [📦 Priority ERP](https://p.priority-connect.online/webui/P009W/#)
    - [🧠 Senior Expert (ChatGPT)](https://chatgpt.com/)
    """)
else:
    with open(f"{app_file}.py", "r", encoding="utf-8") as f:
        exec(f.read(), globals())

# ===============================
# Footer
# ===============================
st.markdown("---")
st.markdown("🧑‍💻 Developed by: **Sergey Minchin** – **Polytex Service Team**")
st.markdown("📧 sergeym@polytex.co.il")
st.markdown("📅 April 2025")
