import streamlit as st
from streamlit_showcase_main_page import data
st.title('first page of Egypt High School Data Analysis 2022 🏫')


st.write(data.head(5))
