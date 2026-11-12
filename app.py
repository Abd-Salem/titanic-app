import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.io as pio
from utils.data import load_data
from utils.figures import plot_family_size, plot_outcome, plot_heatmap

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


st.title("Titanic Explorer", text_alignment='center')

left, mid, right = st.columns([1, 2, 1])
with mid:
    st.image('utils/titanic.jpeg', use_container_width=True)


st.set_page_config(layout='wide')

show_data = st.checkbox("Show data")
if show_data:
    st.dataframe(df.head(10), hide_index=True)



classes = st.multiselect("Select classes", df["class"].unique(), default=df["class"].unique())
gender = st.radio("Select gender", ["All", "Male", "Female"], horizontal=True)

if gender == "All":
    data = df[df["class"].isin(classes)]
else:
    data = df[(df["class"].isin(classes)) & (df["sex"] == gender)]

c1_1, c2_1, c3_1, c4_1 = st.columns(4)
with c1_1:
    st.metric("Total passengers", len(data))
with c2_1:
    st.metric("Survived Rate", f"{len(data[data['survival'] == 'Survived']) / len(data) * 100:.1f}%")
with c3_1:
    st.metric("Median Age", round(data["age"].median(), 1))
with c4_1:
    st.metric("Median Fare", round(data["fare"].median(), 1))



tab1, tab2 = st.tabs(['heatmap', 'Family size Vs outcome'])

with tab1:
    c1, c2 = st.columns(2)

    with c1:
        st.plotly_chart(plot_family_size(data), use_container_width=True)
    with c2:
        st.plotly_chart(plot_outcome(data), use_container_width=True)

with tab2:
    st.plotly_chart(plot_heatmap(data), use_container_width=True)


# c1,c2 = st.columns(2)

# with c1:
#     fig = plot_family_size(data)
#     st.plotly_chart(fig, use_container_width=True)

# with c2:
#     fig = plot_outcome(data)
#     st.plotly_chart(fig, use_container_width=True)