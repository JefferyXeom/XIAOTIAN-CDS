###
# python=3.8.5
# version=0.0.1
# workspace_root=$(project_root)
###

import pandas as pd
import numpy as np
import plotly.graph_objs as go

# Load the Excel file
file_path = "../materials/赛道一：小、微无人机集群目标跟踪/点迹数据1-公开提供.xlsx"  # Update this to the correct file path
df = pd.read_excel(file_path)

# Filter the data for only the first 5 loops (圈数 <= 5)
loops_data = df[df["圈数"] <= 5].reset_index(drop=True)

# Convert spherical coordinates to Cartesian coordinates
r = loops_data["斜距(m)"]
theta = np.deg2rad(loops_data["方位角（°）"])  # Convert degrees to radians
phi = np.deg2rad(loops_data["俯仰角（°）"])  # Convert degrees to radians

# Calculate Cartesian coordinates
x = r * np.cos(theta) * np.cos(phi)
y = r * np.sin(theta) * np.cos(phi)
z = r * np.sin(phi)

# Prepare the data for KNN clustering
xyz_data = np.vstack((x, y, z)).T

# Create a color map for each loops
colors = ["red", "blue", "green", "orange", "purple"]

# Create traces for each cluster
traces = []

total_loops = 1 # for there is only 5 colors, this variable should be <=5
# Loop over the first ${total_loops} and create a separate trace for each
for loop_number in range(1, total_loops + 1):
    loop_data = loops_data[loops_data["圈数"] == loop_number]

    # Convert spherical coordinates to Cartesian coordinates
    r = loop_data["斜距(m)"]
    theta = np.deg2rad(loop_data["方位角（°）"])  # Convert degrees to radians
    phi = np.deg2rad(loop_data["俯仰角（°）"])  # Convert degrees to radians

    # Calculate Cartesian coordinates
    x = r * np.cos(theta) * np.cos(phi)
    y = r * np.sin(theta) * np.cos(phi)
    z = r * np.sin(phi)

    # Create a 3D scatter plot trace for this loop
    if total_loops == 1:
        marker_dict = dict(size=5, color=r, opacity=0.8)
    else:
        marker_dict = dict(size=5, color=colors[loop_number - 1], opacity=0.8)
    trace = go.Scatter3d(
        x=x,
        y=y,
        z=z,
        mode="markers",
        marker=marker_dict,
        name=f"Loop {loop_number}",
        text=[
            f"Loop: {loop_number}<br>Range: {dist}m<br>Azimuth: {azim}°<br>Pitch: {pitch}°"
            for dist, azim, pitch in zip(
                r, loop_data["方位角（°）"], loop_data["俯仰角（°）"]
            )
        ],
        hoverinfo="text",
    )

    traces.append(trace)


# Reference azimuth line (horizontal)
azimuth_line = go.Scatter3d(
    x=[0, np.max(x)],
    y=[0, 0],
    z=[0, 0],
    mode="lines",
    line=dict(color="blue", width=4),
    name="Azimuth Line",
)

# Reference pitch line (vertical)
pitch_line = go.Scatter3d(
    x=[0, 0],
    y=[0, 0],
    z=[0, np.max(z)],
    mode="lines",
    line=dict(color="red", width=4),
    name="Pitch Line",
)

# Add reference lines to traces
traces.extend([azimuth_line, pitch_line])

# Create the layout for the 3D plot
layout = go.Layout(
    title="Radar Data Points with Clustering and Reference Lines",
    scene=dict(
        xaxis=dict(title="X (meters)"),
        yaxis=dict(title="Y (meters)"),
        zaxis=dict(title="Z (meters)"),
    ),
    showlegend=True,
)

# Create the figure with all traces
fig = go.Figure(data=traces, layout=layout)

# Show the interactive plot
fig.show()