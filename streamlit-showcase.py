import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.title('Egypt High School Data Analysis 2022 🏫')

data_url = 'https://storage.googleapis.com/kaggle-data-sets/2535553/4585335/compressed/High_School_Public_Results_2022_EG_both_attempts.csv.zip?X-Goog-Algorithm=GOOG4-RSA-SHA256&X-Goog-Credential=gcp-kaggle-com%40kaggle-161607.iam.gserviceaccount.com%2F20221130%2Fauto%2Fstorage%2Fgoog4_request&X-Goog-Date=20221130T104636Z&X-Goog-Expires=259200&X-Goog-SignedHeaders=host&X-Goog-Signature=a42f5e4a67791e0d4607e86d0fc4584608ec1aae241fdda8e2e2b7fd301349de6e1b5cb7d70255f544a719d449aa831e82fbe7c270df050370a8bbb8b794e96425d83c5d779d7bb9083b06ea7ee0999e8f83e6ec3798610a0bcfb2344b3804453481b5ce073325a911ac29280e606e6fd772133c7f7690991d896c80c3d448c8a137861383d4d36b4f1755eeaa9b8f3e524cd6cb65bf144f222f5c1c59b34324480028ac7c60e7859dab9024acf29f2eb377f2c25d7ed1d0d971f02ee599bc1541153a85c53bf8fc16a4286726776ae723668f0262bee1ab0defdce94926732c757e73928807ba449c636dd04e8da1b9c9cb58db3773fd253a2e490e95f3efb9'


@st.cache
def load_data(data_url):
    data = pd.read_csv(data_url, compression='zip')
    return data


data_load_state = st.text('Loading data...')
data = load_data(data_url)
data_load_state.text('Loading data...done!')

st.header('Top 10 schools for each districts')

city = st.selectbox('Select city:', data['city'].unique())
branch = st.selectbox('Select branch:', data['branch'].unique()) 

data_subset = data.loc[(data['city'] == city) & (data['branch'] == branch)]
data_subset = data_subset.groupby('school_name')['Percentage'].mean().sort_values(ascending=False)
data_subset = data_subset.rename('Average Percentage')

st.bar_chart(data=data_subset.head(10))

#st.write(data_subset)


