#!/usr/bin/env python3
import pandas as pd
import plotly.graph_objects as go

fig = go.Figure()

for i, (f, l) in enumerate(
    [
        ("cores", "Number of logical cores"),
        ("frequency", "Frequency (MHz)"),
        ("specint", "Single-thread performance (SpecINT x 1000)"),
        ("watts", "Typical power (Watts)"),
        ("transistors", "Transistors (thousands)"),
    ]
):
    df = pd.read_csv(
        f"microprocessor-trend-data/{f}.dat", sep="\s+", skiprows=0, names=["year", f]
    )
    fig.add_trace(
        go.Scatter(
            name=l,
            x=df["year"],
            y=df[f],
            mode="markers",
            marker_symbol=i,
            dx=10,
            hovertemplate="%{y:.2f}<extra></extra>",
        )
    )

fig.update_layout(
    title="50 years of microprocessor trend data",
    xaxis_title="Year",
    width=800,
    height=400,
    yaxis=dict(type="log", showexponent="all", exponentformat="power", dtick=1),
)

fig.write_json("microprocessor-trend-data.json")
