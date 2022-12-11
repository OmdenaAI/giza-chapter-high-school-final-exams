import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px 


st.title("Deploy Our Data")
st.header("Get your Result")
df=pd.read_csv('03_firstExam_data_english_G_v1.3.csv')

df['Percentage'] = (df['Percentage'].str.strip('%').astype(float))
print (df.info())


input_seat_no=st.text_input("Enter your seat_no: ")
if st.button("apply"):
    #print(df,input_seat_no)

    def display(df,input_seat_no):
        if input_seat_no in df['desk_no']:
            y = df['desk_no'].iloc[0: , : -1]
            print(y)
            st.write(st.subheader('Your precentage is {}'.format(y)))
    display(df,input_seat_no)

col1, col2, col3 ,col4= st.columns(4)
with col1:
    city=st.selectbox('select_city', df['government_Arabic'].unique())
with col2:
    branch=st.selectbox('select_branch',df['branch'].unique())
with col3:
    adminstrate= st.selectbox('select_adminstration',df['administration_Arabic'].unique())
with col4:
    no_schools=st.slider('No-of_school',min_value=1,max_value=30,step=1,value=10)

data_subset=df.loc[(df['government_Arabic'] == city)&(df['branch']== branch)]     
data_subset=data_subset.groupby('schoolName_Arabic')['Percentage'].mean().sort_values(ascending=False).head( no_schools)
st.write(data_subset)



#visualization

fig= px.bar(
    data_subset, y=data_subset, x='Percentage',orientation='h',
    labels = ['school_name','percentage','Average_percentage'],
    color_discrete_sequence = ['#F63366']
)
st.plotly_chart(fig)


