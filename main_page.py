import streamlit as st
import pandas as pd
import plotly.express as px

st.title('Egypt High School Data Analysis 2022 🏫')

data_location = "dataset\High_School_Public_Results_2022_EG_both_attempts.csv.zip"

@st.cache
def load_data(data_location):
    data = pd.read_csv(data_location, compression='zip')
    return data


with st.spinner('Preparing data...'):
    data = load_data(data_location)

col1, col2, col3 = st.columns(3)
with col1:
    city = st.selectbox('Select city:', data['city'].unique())
with col2:
    branch = st.selectbox('Select branch:', data['branch'].unique()) 
with col3:
    no_schools = st.slider("Number of schools:", min_value=1, max_value=50, step=1, value=10)

st.header(f'Top {no_schools} schools in \'{city}\' for \'{branch}\' branch   ')



data_subset = data.loc[(data['city'] == city) & (data['branch'] == branch)]
data_subset = data_subset.groupby('school_name')['Percentage'].median().sort_values(ascending=False).head(no_schools)
fig = px.bar(
    data_subset, y=data_subset.index, x='Percentage', orientation='h',
    labels={'school_name':'','Percentage':'Average Percentage'},
    color_discrete_sequence=['#F63366']
    )

fig.update_layout(yaxis=dict(autorange="reversed"))
fig.update_layout(title_text='School names', title_x=0.5)

st.plotly_chart(fig)


