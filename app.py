import pandas as pd
import dash
from dash import dcc, html
import plotly.express as px

# Load processed data
df = pd.read_csv("formatted_output.csv")

# Ensure date column is parsed as datetime
df["date"] = pd.to_datetime(df["date"])

# Aggregate sales by date
daily_sales = df.groupby("date")["sales"].sum().reset_index()

# Create line chart
fig = px.line(
    daily_sales,
    x="date",
    y="sales",
    title="Pink Morsel Sales Over Time",
    labels={"date": "Date", "sales": "Total Sales"}
)

# Add vertical line for price increase on 15 Jan 2021
fig.add_shape(
    type="line",
    x0="2021-01-15", x1="2021-01-15",
    y0=0, y1=1,
    xref="x", yref="paper",
    line=dict(color="red", width=2, dash="dash")
)

# Add annotation text
fig.add_annotation(
    x="2021-01-15",
    y=1,
    xref="x",
    yref="paper",
    text="Price Increase",
    showarrow=False,
    yanchor="bottom"
)

# Initialise Dash app
app = dash.Dash(__name__)

# Layout
app.layout = html.Div([
    html.H1("Soul Foods: Pink Morsel Sales Visualiser", style={"textAlign": "center"}),

    dcc.Graph(
        id="sales-line-chart",
        figure=fig
    )
])

# Run server
if __name__ == "__main__":
    app.run(debug=True)
