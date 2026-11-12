import plotly.express as px
from .config import COLORS, ORDERS


def plot_family_size(data):
    fig = px.histogram(data, x="family_size", nbins=11, labels={"family_size": "Family size (incl. the passenger)"},
                   title="How big were the families on board?")
    fig.update_layout(bargap=0.1, yaxis_title="Passengers")
    return fig


def plot_outcome(data):
    outcome = data["survival"].value_counts().reset_index()

    fig = px.pie(outcome, names="survival", values="count", hole=0.5, color="survival",
                color_discrete_map=COLORS, title="Died vs survived")

    return fig

def plot_heatmap(data):
    rate = data.pivot_table(index="sex", columns="class", values="survived", aggfunc="mean")

    fig = px.imshow(rate, text_auto=".0%", zmin=0, zmax=1, color_continuous_scale="Teal",
                    labels={"x": "Class", "y": "Sex", "color": "Survival rate"},
                    title="Survival rate by sex and class")
    return fig