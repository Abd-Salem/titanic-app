import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.io as pio
from utils.data import load_data
from utils.figures import plot_family_size, plot_outcome

pio.renderers.default = "plotly_mimetype+notebook_connected"   # plotly.js is loaded from the internet: the saved notebook stays small

df = load_data()

df.columns = df.columns.str.lower()
df["class"] = df["pclass"].map({1: "First", 2: "Second", 3: "Third"})
df["survival"] = df["survived"].map({0: "Died", 1: "Survived"})
df["port"] = df["embarked"].map({"C": "Cherbourg", "Q": "Queenstown", "S": "Southampton"})
df["family_size"] = df["sibsp"] + df["parch"] + 1
df["title"] = df["name"].str.extract(r",\s*([^\.]+)\.", expand=False)
df["age_group"] = pd.cut(df["age"], [0, 12, 18, 35, 60, 80],
                         labels=["child", "teen", "young adult", "adult", "senior"])


st.title("Titanic Explorer")

left, mid, right = st.columns([1, 2, 1])
with mid:
    st.image('utils/titanic.jpeg', use_container_width=True)


st.set_page_config(layout='wide')

show_data = st.checkbox("Show data")
if show_data:
    st.dataframe(df.head(10), hide_index=True)

classes = st.multiselect("Select classes", df["class"].unique(), default=df["class"].unique())
gender = st.radio("Select gender", ["male", "female"], horizontal=True)

data = df[(df["class"].isin(classes)) & (df["sex"] == gender)]

c1_metric, c2_metric, c3_metric, c4_metric = st.columns(4)

with c1_metric:
    st.metric(f'Total Passengers: {len(data)}')

with c2_metric:
    st.metric(f'Survived Rate: {len(data[data['survival'] == 'survived']) / len(df) * 100:.1f}')


with c3_metric:
    st.metric(f"Medium Age: {round(df['age'].median(), 1)}")

with c4_metric:
    st.metric(f'Median Fare: {round(df['fare'].median(), 1)}')


fig1 = plot_family_size(data)
st.plotly_chart(fig1, use_container_width=True)

fig2 = plot_outcome(data)
st.plotly_chart(fig2, use_container_width=True)


# c1,c2 = st.columns(2)

# with c1:
#     fig = plot_family_size(data)
#     st.plotly_chart(fig, use_container_width=True)

# with c2:
#     fig = plot_outcome(data)
#     st.plotly_chart(fig, use_container_width=True)