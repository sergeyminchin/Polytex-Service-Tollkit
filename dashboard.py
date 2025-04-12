import streamlit as st
import pandas as pd
import plotly.express as px
from PIL import Image
import io

# Load and display logo
logo = Image.open("logo.png")
st.image(logo, use_container_width=False)

# Load preprocessed data
total_calls_summary = pd.DataFrame({
    'Year': ['Q1 2024', 'Q1 2025'],
    'Total Calls': [507, 609],
    'Change (%)': [None, 20.12]
})

# Repeated Calls by Technician
repeated_2024 = pd.read_excel('ניתוח קריאות 2024 Q1.xlsx', sheet_name='קריאות חוזרות לפי טכנאי').assign(Year='2024')
repeated_2025 = pd.read_excel('Service Calls Q1_2025_final.xlsx', sheet_name='קריאות חוזרות לפי טכנאי').assign(Year='2025')
combined_repeated_calls = pd.concat([repeated_2024, repeated_2025])

# Technician Performance Summary
performance_2024 = repeated_2024[['טכנאי', 'קריאות חוזרות', 'סה"כ ביקורים']].copy()
performance_2024['אחוז חוזרות'] = (performance_2024['קריאות חוזרות'] / performance_2024['סה"כ ביקורים'] * 100).round(2)
performance_2024['שנה'] = '2024'

performance_2025 = repeated_2025[['טכנאי', 'קריאות חוזרות', 'סה"כ ביקורים']].copy()
performance_2025['אחוז חוזרות'] = (performance_2025['קריאות חוזרות'] / performance_2025['סה"כ ביקורים'] * 100).round(2)
performance_2025['שנה'] = '2025'

technician_performance = pd.concat([performance_2024, performance_2025])

# Calls by Type (with index fix)
calls_by_type_2024 = pd.read_excel('ניתוח קריאות 2024 Q1.xlsx', sheet_name='התפלגות סוגי קריאה', index_col=0).reset_index()
calls_by_type_2025 = pd.read_excel('Service Calls Q1_2025_final.xlsx', sheet_name='התפלגות סוגי קריאה', index_col=0).reset_index()
calls_by_type_2024['Year'] = '2024'
calls_by_type_2025['Year'] = '2025'
calls_by_type = pd.concat([calls_by_type_2024, calls_by_type_2025])
calls_by_type.rename(columns={calls_by_type.columns[0]: 'סוג קריאה'}, inplace=True)

# Parts Usage
parts_usage_2024 = pd.read_excel('ניתוח קריאות 2024 Q1.xlsx', sheet_name='חלקים הכי נפוצים').assign(Year='2024')
parts_usage_2025 = pd.read_excel('Service Calls Q1_2025_final.xlsx', sheet_name='חלקים הכי נפוצים').assign(Year='2025')
combined_parts_usage = pd.concat([parts_usage_2024, parts_usage_2025])

# Most Common Faults
faults_2024 = pd.read_excel('ניתוח קריאות 2024 Q1.xlsx', sheet_name='תקלות לפי דגם').assign(Year='2024')
faults_2025 = pd.read_excel('Service Calls Q1_2025_final.xlsx', sheet_name='תקלות לפי דגם').assign(Year='2025')
combined_faults = pd.concat([faults_2024, faults_2025])

# Calls by Site
calls_by_site_2024 = pd.read_excel('ניתוח קריאות 2024 Q1.xlsx', sheet_name='קריאות לפי אתר').assign(Year='2024')
calls_by_site_2025 = pd.read_excel('Service Calls Q1_2025_final.xlsx', sheet_name='קריאות לפי אתר').assign(Year='2025')
combined_calls_by_site = pd.concat([calls_by_site_2024, calls_by_site_2025])

# Technical Visits by Model
visits_by_model_2024 = pd.read_excel('ניתוח קריאות 2024 Q1.xlsx', sheet_name='ביקורים טכניים לפי דגם').assign(Year='2024')
visits_by_model_2025 = pd.read_excel('Service Calls Q1_2025_final.xlsx', sheet_name='ביקורים טכניים לפי דגם').assign(Year='2025')
combined_visits_by_model = pd.concat([visits_by_model_2024, visits_by_model_2025])

# Define Polytex colors
polytex_colors = ['#f46c04', '#003B70']

# Streamlit App
st.title('Service Calls Comparison Dashboard: Q1 2024 vs Q1 2025')

# Total Calls Summary
st.subheader('Overall Calls Summary')
st.dataframe(total_calls_summary)

# Export Summary
output_buffer = io.BytesIO()
with pd.ExcelWriter(output_buffer, engine='xlsxwriter') as writer:
    total_calls_summary.to_excel(writer, sheet_name='Total Calls', index=False)
    technician_performance.to_excel(writer, sheet_name='Technician Performance', index=False)
st.download_button(label="Download Summary Report", data=output_buffer.getvalue(), file_name="Q1_Comparison_Summary.xlsx")

fig_total = px.bar(total_calls_summary, x='Year', y='Total Calls', text='Total Calls', 
                   title='Total Calls: Q1 2024 vs Q1 2025', color='Year',
                   color_discrete_sequence=polytex_colors)
st.plotly_chart(fig_total)

# Technician Performance Summary
st.subheader("Technician Performance Summary")
st.dataframe(technician_performance)

# Interactive Technician Analysis
st.subheader('Repeated Calls Analysis by Technician')
tech_list = combined_repeated_calls['טכנאי'].unique()
selected_tech = st.selectbox('Select Technician', options=['All'] + tech_list.tolist())

if selected_tech != 'All':
    filtered_df = combined_repeated_calls[combined_repeated_calls['טכנאי'] == selected_tech]
else:
    filtered_df = combined_repeated_calls

fig_repeated = px.bar(filtered_df, x='טכנאי', y='קריאות חוזרות', color='Year',
                      barmode='group',
                      title=f'Repeated Calls by Technician: {selected_tech if selected_tech != "All" else "All Technicians"}',
                      color_discrete_sequence=polytex_colors)
st.plotly_chart(fig_repeated)

# Calls by Type Comparison
st.subheader('Service Calls by Type Comparison')
type_list = calls_by_type['סוג קריאה'].unique()
selected_type = st.selectbox('Select Call Type', options=['All'] + type_list.tolist())

if selected_type != 'All':
    filtered_type_df = calls_by_type[calls_by_type['סוג קריאה'] == selected_type]
else:
    filtered_type_df = calls_by_type

fig_type = px.bar(filtered_type_df, x='סוג קריאה', y='count', color='Year',
                  barmode='group',
                  title=f'Service Calls by Type: {selected_type if selected_type != "All" else "All Types"}',
                  color_discrete_sequence=polytex_colors)
st.plotly_chart(fig_type)

# Parts Usage Comparison
st.subheader('Most Used Parts Comparison')
part_list = combined_parts_usage[combined_parts_usage.columns[0]].unique()
selected_part = st.selectbox('Select Part', options=['All'] + part_list.tolist())

if selected_part != 'All':
    filtered_parts_df = combined_parts_usage[combined_parts_usage[combined_parts_usage.columns[0]] == selected_part]
else:
    filtered_parts_df = combined_parts_usage

fig_parts = px.bar(filtered_parts_df, x=filtered_parts_df.columns[0], y=filtered_parts_df.columns[1], color='Year',
                   barmode='group',
                   title=f'Usage of Part: {selected_part if selected_part != "All" else "All Parts"}',
                   color_discrete_sequence=polytex_colors)
st.plotly_chart(fig_parts)

# Most Common Faults Comparison
st.subheader('Most Common Faults by Model')
fault_name_col = combined_faults.columns[0]
fault_count_col = combined_faults.columns[1]
fault_list = combined_faults[fault_name_col].unique()
selected_fault = st.selectbox('Select Fault Type', options=['All'] + fault_list.tolist())

if selected_fault != 'All':
    filtered_faults = combined_faults[combined_faults[fault_name_col] == selected_fault]
else:
    filtered_faults = combined_faults

fig_faults = px.bar(filtered_faults, x=fault_name_col, y=fault_count_col, color='Year',
                    barmode='group',
                    title=f'Occurrences of Fault: {selected_fault if selected_fault != "All" else "All Faults"}',
                    color_discrete_sequence=polytex_colors)
st.plotly_chart(fig_faults)

# Calls by Site Comparison
st.subheader('Service Calls by Site')
site_col = combined_calls_by_site.columns[0]
site_count_col = combined_calls_by_site.columns[1]
site_list = combined_calls_by_site[site_col].unique()
selected_site = st.selectbox('Select Site', options=['All'] + site_list.tolist())

if selected_site != 'All':
    filtered_sites = combined_calls_by_site[combined_calls_by_site[site_col] == selected_site]
else:
    filtered_sites = combined_calls_by_site

fig_sites = px.bar(filtered_sites, x=site_col, y=site_count_col, color='Year',
                   barmode='group',
                   title=f'Service Calls for Site: {selected_site if selected_site != "All" else "All Sites"}',
                   color_discrete_sequence=polytex_colors)
st.plotly_chart(fig_sites)

# Technical Visits by Model
st.subheader('Technical Visits by Model')
model_col = combined_visits_by_model.columns[0]
visit_col = combined_visits_by_model.columns[1]
model_list = combined_visits_by_model[model_col].unique()
selected_model = st.selectbox('Select Model', options=['All'] + model_list.tolist())

if selected_model != 'All':
    filtered_models = combined_visits_by_model[combined_visits_by_model[model_col] == selected_model]
else:
    filtered_models = combined_visits_by_model

fig_visits = px.bar(filtered_models, x=model_col, y=visit_col, color='Year',
                    barmode='group',
                    title=f'Technical Visits for Model: {selected_model if selected_model != "All" else "All Models"}',
                    color_discrete_sequence=polytex_colors)
st.plotly_chart(fig_visits)

# Call Types per Technician
st.subheader("Call Types per Technician")
calls_by_tech_2024 = pd.read_excel('ניתוח קריאות 2024 Q1.xlsx', sheet_name='קריאות לפי טכנאי וסוג קריאה').assign(Year='2024')
calls_by_tech_2025 = pd.read_excel('Service Calls Q1_2025_final.xlsx', sheet_name='קריאות לפי טכנאי וסוג קריאה').assign(Year='2025')
combined_calls_by_tech = pd.concat([calls_by_tech_2024, calls_by_tech_2025])
combined_calls_by_tech['סוג קריאה'] = combined_calls_by_tech['סוג קריאה'].replace('תחזוקה', 'תחזוקה/שיפוץ/בדיקה')

type_option = st.selectbox('Group by Call Type:', ['All Types'] + combined_calls_by_tech['סוג קריאה'].unique().tolist())

if type_option != 'All Types':
    filtered_call_type = combined_calls_by_tech[combined_calls_by_tech['סוג קריאה'] == type_option]
else:
    filtered_call_type = combined_calls_by_tech

fig_calls_type = px.bar(filtered_call_type, x='לטיפול', y='כמות קריאות', color='Year',
                        barmode='group',
                        title=f'Calls by Technician - Type: {type_option}',
                        color_discrete_sequence=polytex_colors)
st.plotly_chart(fig_calls_type)