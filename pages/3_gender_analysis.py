from main_page import data
import plotly.express as px
import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd

@st.cache
def get_f1_data(exam_trial: str, df: pd.DataFrame):
    if exam_trial == "First Exam Trial":
        f1_target_col = "Percentage"
    else:
        f1_target_col = "Percentage_2nd"
    return df[["branch", "gender", f1_target_col]].groupby(["branch", "gender"], as_index=False).median(), f1_target_col

@st.cache
def get_f2_data(exam_trial: str, df: pd.DataFrame):
    if exam_trial == "First Exam Trial":
        f2_mask = df["_merge"] == "left_only"
    else:
        f2_mask = (df["_merge"] == "right_only") | (df["_merge"] == "both")
    return data[f2_mask][["branch", "gender", "desk_no"]].groupby(["branch", "gender"], as_index=False).count().sort_values(["branch"])

@st.cache
def get_f3_data(df: pd.DataFrame):
    return data[["status", "gender", "desk_no"]].groupby(["status", "gender"], as_index=False).count().rename({"desk_no": "total students"}, axis=1)

@st.cache
def get_f4_data(exam_trial: str, branch: str, df: pd.DataFrame):
    if exam_trial == "First Exam Trial":
        target_cols = [*df.columns[7:24]]
        target_cols.remove("total")
    else:
        target_cols = [*df.columns[27:44]]
        target_cols.remove("total_2nd")

    f4_data = pd.melt(df[df["branch"] == branch], id_vars=["branch", "gender"], value_vars=target_cols)
    f4_data.rename({"variable": "topic", "value": "grade"}, inplace=True, axis=1)
    f4_data = f4_data.groupby(["branch", "gender", "topic"], as_index=False).median().dropna(axis=0, how="any")
    return f4_data

gender_color = {'M': '#6379F2', 'F': '#F24C3D'}
trials_dict = {"left_only": "first trial", "both": "second trial"}

#------------ fig 3 --------------------
f3_data = get_f3_data(df=data)
fig3 = px.sunburst(f3_data,
            path=["status", "gender"], values="total students",
            color="gender", color_discrete_map=gender_color)
fig3.update_traces(textinfo="label+percent parent", hovertemplate=('<b>Total Number of Students: </b>: %{value}'))
fig3.update_layout(title_text="Students Passing Status", title_x=0.5)
st.plotly_chart(fig3)
#----------------------------------------

#------------ fig 1 --------------------
f1_trial = st.selectbox('Exam Trial:', ["First Exam Trial", "Second Exam Trial"], key="sb1")
f1_data, f1_target_col = get_f1_data(exam_trial=f1_trial, df=data)
fig1 = px.bar(f1_data,
            x="branch", y=f1_target_col,
            color='gender',
            color_discrete_map=gender_color,
            barmode='group')

fig1.update_layout(title_text="Students Total Percentage Median", title_x=0.5)
st.plotly_chart(fig1)
#----------------------------------------

#------------ fig 2 --------------------
f2_trial = st.selectbox('Exam Trial:', ["First Exam Trial", "Second Exam Trial"], key="sb2")
f2_data = get_f2_data(exam_trial=f2_trial, df=data)
annotations = []
x_positions = [0.12, 0.5, 0.92]
fig2 = make_subplots(rows=1, cols=3, specs=[[{"type": "pie"}, {"type": "pie"}, {"type": "pie"}]])
for i, branch in enumerate(f2_data["branch"].unique()):
    branch_filter = f2_data["branch"] == branch
    subplot = go.Pie(labels=f2_data[branch_filter]["gender"],
        values= f2_data[branch_filter]["desk_no"],
        name=branch,
        marker_colors=f2_data["gender"].map(gender_color)
        )
    fig2.add_trace(subplot, 1, i + 1)
    annotations.append(dict(text=branch, x=x_positions[i], y=0.5, font_size=16, showarrow=False))

fig2.update_traces(hole=.5, hoverinfo="label+percent")
fig2.update_layout(title_text="Gender Distribution on each Branch", annotations=annotations, title_x=0.5)
st.plotly_chart(fig2)
#----------------------------------------

#------------ fig 4 --------------------
col1, col2 = st.columns(2)
with col1:
    f4_trial = st.selectbox('Exam Trial:', ["First Exam Trial", "Second Exam Trial"], key="sb4")
with col2:
    f4_branch = st.selectbox('Branch:', data["branch"].unique())

f4_data = get_f4_data(exam_trial=f4_trial, branch=f4_branch, df=data)
fig4 = px.bar(f4_data,
            x="grade", y="topic", orientation="h",
            color='gender',
            color_discrete_map=gender_color,
            barmode='group',
            height=600)

fig4.update_layout(title_text=f'Median Topics Grade for "{f4_branch}" Branch', title_x=0.5)
st.plotly_chart(fig4)
#----------------------------------------