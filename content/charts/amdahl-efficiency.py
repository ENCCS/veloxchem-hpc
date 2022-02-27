#!/usr/bin/env python3
import numpy as np
import plotly.graph_objs as go

serial_fraction = [0.001, 0.01, 0.1, 0.3, 0.5]
workers = np.around(np.geomspace(1, 2048, num=12)).astype(int)
fig = go.Figure()

for i, f in enumerate(serial_fraction):
    efficiency = 1 / np.multiply(workers, (f + (1 - f) / workers))
    fig.add_trace(
        go.Scatter(
            name=f"{f*100}%",
            x=workers,
            y=efficiency,
            mode="lines+markers",
            marker_symbol=i,
            hovertemplate="~%{y:.2%}<extra></extra>",
        )
    )

fig.update_layout(
    title="Efficiency according to Amdahl's law",
    hovermode="x unified",
    xaxis_title="Number of workers",
    yaxis_title="Efficiency",
    width=600,
    height=600,
    xaxis=dict(type="log", dtick=np.log10(2)),
    yaxis=dict(tickformat=".0%"),
    legend=dict(title="Serial fraction"),
)

fig.write_json("amdahl-efficiency.json")
