import pandas as pd
from dash import Dash, html, dcc, Input, Output
import plotly.express as px

# Path to formatted data
DATA_PATH = "./formatted_output.csv"

# Load data
data = pd.read_csv(DATA_PATH)
data["date"] = pd.to_datetime(data["date"])
data = data.sort_values(by="date")

# Initialize app
app = Dash(__name__)

# Define color palette
colors = {
    "background": "#f5f7fa",
    "card": "#ffffff",
    "header": "#2c3e50",
    "subheader": "#7f8c8d",
    "accent": "#e91e63",
    "text": "#2d3436"
}

# Layout
app.layout = html.Div(
    style={"backgroundColor": colors["background"], "fontFamily": "Segoe UI, sans-serif", "padding": "30px"},
    children=[

        # Header section
        html.Div(
            style={
                "textAlign": "center",
                "marginBottom": "40px",
                "backgroundColor": colors["card"],
                "padding": "20px",
                "borderRadius": "12px",
                "boxShadow": "0 4px 8px rgba(0,0,0,0.1)"
            },
            children=[
                html.H1("🌸 Pink Morsel Sales Dashboard",
                        style={"color": colors["header"], "marginBottom": "10px"}),
                html.P("Interactive visualisation to explore sales trends before and after the price increase",
                       style={"color": colors["subheader"], "fontSize": "16px"})
            ]
        ),

        # Region filter card
        html.Div(
            style={
                "backgroundColor": colors["card"],
                "padding": "20px",
                "borderRadius": "12px",
                "marginBottom": "30px",
                "boxShadow": "0 4px 8px rgba(0,0,0,0.05)"
            },
            children=[
                html.Label("🔍 Filter by Region:",
                           style={"fontWeight": "bold", "color": colors["text"], "fontSize": "16px"}),
                dcc.RadioItems(
                    id="region-selector",
                    options=[
                        {"label": "All", "value": "all"},
                        {"label": "North", "value": "north"},
                        {"label": "East", "value": "east"},
                        {"label": "South", "value": "south"},
                        {"label": "West", "value": "west"}
                    ],
                    value="all",
                    inline=True,
                    style={"marginTop": "10px", "color": colors["text"], "fontSize": "15px"}
                )
            ]
        ),

        # Graph card
        html.Div(
            style={
                "backgroundColor": colors["card"],
                "padding": "20px",
                "borderRadius": "12px",
                "boxShadow": "0 6px 12px rgba(0,0,0,0.1)"
            },
            children=[
                dcc.Graph(id="sales-graph", style={"height": "600px"})
            ]
        )
    ]
)


# Callback for updating chart
@app.callback(
    Output("sales-graph", "figure"),
    Input("region-selector", "value")
)
def update_chart(selected_region):
    if selected_region == "all":
        filtered_data = data
    else:
        filtered_data = data[data["region"].str.lower() == selected_region]

    fig = px.line(
        filtered_data,
        x="date",
        y="sales",
        color="region" if selected_region == "all" else None,
        markers=True,
        title="Pink Morsel Sales Over Time",
        labels={"date": "Date", "sales": "Total Sales"}
    )

    # Add vertical line for price increase (Jan 15, 2021)
    fig.add_shape(
        type="line",
        x0="2021-01-15",
        x1="2021-01-15",
        y0=0,
        y1=1,
        xref="x",
        yref="paper",
        line=dict(color=colors["accent"], width=2, dash="dash"),
    )

    # Add annotation for the line
    fig.add_annotation(
        x="2021-01-15",
        y=1,
        yref="paper",
        text="Price Increase",
        showarrow=False,
        font=dict(color=colors["accent"], size=12),
        xanchor="left"
    )

    # Style chart
    fig.update_layout(
        plot_bgcolor="white",
        paper_bgcolor=colors["card"],
        font=dict(color=colors["text"], size=14),
        title=dict(x=0.5, font=dict(size=22, color=colors["accent"])),
        xaxis=dict(showgrid=True, gridcolor="lightgrey"),
        yaxis=dict(showgrid=True, gridcolor="lightgrey"),
        margin=dict(l=40, r=40, t=80, b=40),
        transition_duration=500  # smooth animation
    )

    return fig


# Entry point
if __name__ == "__main__":
    app.run(debug=True)
