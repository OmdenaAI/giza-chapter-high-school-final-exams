import streamlit as st
from main_page import data
import plotly.express as px

st.title('Second attempt results analysis')
st.subheader('Students who fail in 2 subject or less are applicable to reattempt the test in these subjects')

subject = st.selectbox('Select Subject:', data.columns[7:24].append(data.columns[5:6]))


data_subset  = data.loc[data['_merge'] == 'both']
data_subset['improve in ' + subject] = data_subset[subject + ('_2nd')] - data_subset[subject]
data_subset = data_subset.loc[data_subset['improve in ' + subject].notna()]
data_subset = data_subset.loc[data_subset['improve in ' + subject] > 0]
 
with st.spinner('Analysing data | Drawing graphs...'):
    fig = px.histogram(data_subset, x='improve in ' + subject, color_discrete_sequence=['#F63366'])
    st.write(fig)

st.caption('The graph shows the distrubution of grades gained in the second attempt in respect with first exam')

col1, col2 = st.columns(2)
with col1:
    st.metric(label="Max imrpove", value=str(data_subset['improve in ' + subject].max()), delta=str(round(data_subset['improve in ' + subject].max()-data_subset['improve in ' + subject].mean(),2)))
with col2:
    st.metric(label="Average improve", value=str(round(data_subset['improve in ' + subject].mean(), 2)))