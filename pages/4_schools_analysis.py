from main_page import data
import plotly.express as px
import streamlit as st
import pandas as pd

@st.cache
def get_f1_data(df: pd.DataFrame):
    f1_data = df.drop_duplicates(subset=["desk_no"], keep="first") \
                .groupby(["city"]) \
                .size() \
                .sort_values(ascending=False)
    city_sorter = {city:i for i,city in enumerate(f1_data.keys())}
    return f1_data, city_sorter

@st.cache
def get_f2_data(df: pd.DataFrame, sort_by: str):
    f2_data = pd.DataFrame(
            df.drop_duplicates(subset=["school_name"], keep="first") \
                .groupby(["city"]) \
                .size()
                ).rename({0: "value"}, axis=1)
    f2_data["order"] = f2_data.index.map(sort_by)
    f2_data.sort_values(["order"], inplace=True)
    return f2_data["value"]

@st.cache
def get_f3_data(f1_data: pd.Series, f2_data: pd.Series):
    return f1_data / f2_data

f1_data, city_sorter = get_f1_data(data)
fig1 = px.line(f1_data, width=800)
fig1.update_layout(showlegend=False, title="Number of Students per City", title_x=0.5)
fig1.update_yaxes(title="")
st.plotly_chart(fig1)

f2_data = get_f2_data(data, sort_by=city_sorter)
fig2 = px.line(f2_data, width=800)
fig2.update_layout(showlegend=False, title="Number of Schools per City", title_x=0.5)
fig2.update_yaxes(title="")
st.plotly_chart(fig2)

f3_data = get_f3_data(f1_data, f2_data)
fig3 = px.line(f3_data, width=800)
fig3.update_layout(showlegend=False, title="Students per School Ratio", title_x=0.5)
fig3.update_yaxes(title="")
st.plotly_chart(fig3)