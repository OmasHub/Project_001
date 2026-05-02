import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Page Config
st.set_page_config(page_title="Healthcare Dashboard", layout="wide")

# Title
st.title("🏥 Healthcare Data Analytics Dashboard")
st.markdown("---")

# Load Data
@st.cache_data
def load_data():
    df = pd.read_csv(r"C:\Users\user\OneDrive\Healthcare1.csv")
    chronic_list = ['Anxiety', 'Arthritis', 'Depression', 'Diabetes', 'Thyroid Disorder', 'Hypertension', 'Epilepsy', 'Liver Disease', 'IBS', "Parkinson's", 'Dementia', 'Obesity', 'Anemia', 'Chronic Kidney Disease', 'Heart Disease', 'Asthma', 'Tuberculosis']
    df['Illness_Type'] = df['Disease'].apply(lambda x: 'Chronic' if x in chronic_list else 'Acute/Episodic')
    df['Age_Group'] = pd.cut(df['Age'], bins=[0, 18, 35, 50, 65, 80, 100], 
                             labels=['0-18', '19-35', '36-50', '51-65', '66-80', '80+'])
    return df

df = load_data()

# Sidebar Filters
st.sidebar.header("Filters")
selected_type = st.sidebar.multiselect("Select Illness Type", options=df['Illness_Type'].unique(), default=df['Illness_Type'].unique())
age_range = st.sidebar.slider("Select Age Range", 0, 100, (0, 100))

# Filtering Logic
filtered_df = df[(df['Illness_Type'].isin(selected_type)) & (df['Age'] >= age_range[0]) & (df['Age'] <= age_range[1])]

# KPIs
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Patients", len(filtered_df))
col2.metric("Avg Age", round(filtered_df['Age'].mean(), 1))
col3.metric("Chronic Cases", len(filtered_df[filtered_df['Illness_Type'] == 'Chronic']))
col4.metric("Avg Symptoms", round(filtered_df['Symptom_Count'].mean(), 1))

st.markdown("---")

# Layout: Row 1
c1, c2 = st.columns(2)

with c1:
    st.subheader("Chronic vs. Acute/Episodic Count")
    type_counts = filtered_df['Illness_Type'].value_counts().reset_index()
    type_counts.columns = ['Illness_Type', 'Count']
    fig1 = px.bar(type_counts, x='Illness_Type', y='Count', 
                  color='Illness_Type', 
                  color_discrete_map={'Chronic': '#e74c3c', 'Acute/Episodic': '#3498db'},
                  text='Count')
    st.plotly_chart(fig1, use_container_width=True)

with c2:
    st.subheader("Disease Frequency by Category")
    disease_counts = filtered_df.groupby(['Disease', 'Illness_Type']).size().reset_index(name='Count')
    disease_counts = disease_counts.sort_values(by='Count', ascending=True)
    fig2 = px.bar(disease_counts, y='Disease', x='Count', color='Illness_Type', orientation='h',
                  color_discrete_map={'Chronic': '#e74c3c', 'Acute/Episodic': '#3498db'})
    st.plotly_chart(fig2, use_container_width=True)

# Layout: Row 2
st.markdown("---")
c3, c4 = st.columns(2)

with c3:
    st.subheader("Age Distribution Across Diseases")
    fig3 = px.box(filtered_df, x='Disease', y='Age', color='Illness_Type',
                  color_discrete_map={'Chronic': '#e74c3c', 'Acute/Episodic': '#3498db'})
    st.plotly_chart(fig3, use_container_width=True)

with c4:
    st.subheader("Patient Concentration Heatmap")
    heatmap_data = filtered_df.groupby(['Disease', 'Age_Group']).size().reset_index(name='Count')
    fig4 = px.density_heatmap(heatmap_data, x='Age_Group', y='Disease', z='Count', 
                              color_continuous_scale='YlGnBu', text_auto=True)
    st.plotly_chart(fig4, use_container_width=True)

# Layout: Row 3
st.markdown("---")
c5, c6 = st.columns(2)

with c5:
    st.subheader("Top 15 Most Frequent Diseases")
    top_15 = filtered_df['Disease'].value_counts().head(15).reset_index()
    top_15.columns = ['Disease', 'Count']
    fig5 = px.bar(top_15, x='Count', y='Disease', orientation='h', color='Count', color_continuous_scale='Viridis')
    st.plotly_chart(fig5, use_container_width=True)

with c6:
    st.subheader("Average Symptom Count per Disease")
    avg_symptoms = filtered_df.groupby('Disease')['Symptom_Count'].mean().sort_values(ascending=False).reset_index()
    fig6 = px.bar(avg_symptoms, x='Disease', y='Symptom_Count', color='Symptom_Count', color_continuous_scale='Blues')
    st.plotly_chart(fig6, use_container_width=True)

# Data Table
with st.expander("View Raw Data"):
    st.dataframe(filtered_df)