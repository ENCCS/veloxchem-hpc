#!/usr/bin/env python3
import numpy as np
import plotly.graph_objs as go

serial_fraction = [0.001, 0.01, 0.1, 0.3, 0.5]
workers = np.around(np.geomspace(1, 2048, num=12)).astype(int)
fig = go.Figure()


for i, f in enumerate(serial_fraction):
    speedup = 1 / (f + (1 - f) / workers)
    fig.add_trace(
        go.Scatter(
            name=f"{f*100}%",
            x=workers,
            y=speedup,
            mode="lines+markers",
            marker_symbol=i,
            hovertemplate="~%{y:.2f}x<extra></extra>",
        )
    )

fig.update_layout(
    hovermode="x unified",
    title="Speedup according to Amdahl's law",
    xaxis_title="Number of workers",
    yaxis_title="Speedup",
    height=500,
    width=600,
    xaxis=dict(type="log", dtick=np.log10(2)),
    yaxis=dict(type="log", showexponent="all", exponentformat="power", dtick=1),
    legend=dict(title="Serial fraction"),
)

fig.write_json("amdahl-speedup.json")
