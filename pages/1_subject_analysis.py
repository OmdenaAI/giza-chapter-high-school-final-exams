import streamlit as st
from main_page import data
import plotly.express as px

st.title('Subject distribution analysis between gender')

subject = st.selectbox('Select Subject:', data.columns[7:24].append(data.columns[5:6]))

st.subheader(f'Distribution of {subject} in both genders')
with st.spinner('Analysing data | Drawing graphs...'):
    fig = px.histogram(data, x=subject, color="gender",
    color_discrete_map= {'M':'light blue', 'F': 'pink'}, barmode='overlay',
    nbins=int(data[subject].max()))
    st.write(fig)

st.caption('The graph shows the distrubution of grades and the averages in both genders')

M_mean = round(data[data['gender'] == 'M'][subject].mean(), 2)
F_mean = round(data[data['gender'] == 'F'][subject].mean(), 2)
Both_mean = round(data[subject].mean(),2)

col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="Male Average", value=str(M_mean), delta=str(round(M_mean-Both_mean,2)))
with col2:
    st.metric(label="Female Average", value=str(F_mean), delta=str(round(F_mean-Both_mean, 2)))
with col3:
     st.metric(label="Total Average", value=str(Both_mean))

