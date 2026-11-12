import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.io as pio
from pathlib import Path

DATA = Path(__file__).parent / "data" / "titanic.csv"
df = pd.read_csv(DATA)

pio.renderers.default = "plotly_mimetype+notebook_connected"   # plotly.js is loaded from the internet: the saved notebook stays small

df = pd.read_csv(r"/home/abdallah/workspace/iti-courses/data-exp-prep-vis/labs/streamlit/titanic_app/data/titanic.csv")
df.columns = df.columns.str.lower()
df["class"] = df["pclass"].map({1: "First", 2: "Second", 3: "Third"})
df["survival"] = df["survived"].map({0: "Died", 1: "Survived"})
df["port"] = df["embarked"].map({"C": "Cherbourg", "Q": "Queenstown", "S": "Southampton"})
df["family_size"] = df["sibsp"] + df["parch"] + 1
df["title"] = df["name"].str.extract(r",\s*([^\.]+)\.", expand=False)
df["age_group"] = pd.cut(df["age"], [0, 12, 18, 35, 60, 80],
                         labels=["child", "teen", "young adult", "adult", "senior"])

ORDERS = {"class": ["First", "Second", "Third"], "survival": ["Died", "Survived"],
          "age_group": ["child", "teen", "young adult", "adult", "senior"]}
COLORS = {"Died": "#D95D4A", "Survived": "#0F766E"}


st.title("Titanic app")
st.image('titanic_app/utils/titanic.jpeg')


show_data = st.checkbox("Show data")
if show_data:
    st.dataframe(df.head(10), hide_index=True)

classes = st.multiselect("Select classes", df["class"].unique(), default=df["class"].unique())
gender = st.radio("Select gender", ["male", "female"], horizontal=True)

data = df[(df["class"].isin(classes)) & (df["sex"] == gender)]


c1, c2 = st.columns(2)

with c1:
    fig = px.histogram(data, x="family_size", nbins=11, labels={"family_size": "Family size (incl. the passenger)"},
                   title="How big were the families on board?")
    fig.update_layout(bargap=0.1, yaxis_title="Passengers")
    st.plotly_chart(fig, use_container_width=True)

with c2:
    outcome = data["survival"].value_counts().reset_index()

    fig = px.pie(outcome, names="survival", values="count", hole=0.5, color="survival",
                color_discrete_map=COLORS, title="Died vs survived")
    st.plotly_chart(fig, use_container_width=True)