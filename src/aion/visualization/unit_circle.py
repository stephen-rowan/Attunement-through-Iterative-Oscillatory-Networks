"""Unit circle visualization for AION simulation."""

import numpy as np
import plotly.graph_objects as go


def create_unit_circle_plot(
    phases: list[float],
    resonance_index: float,
) -> go.Figure:
    """
    Create Plotly figure for unit circle visualization.

    Args:
        phases: List of oscillator phases [0, 2π)
        resonance_index: Current R value for display

    Returns:
        Plotly Figure object ready for st.plotly_chart()

    Contract:
        - Figure shows unit circle with oscillators as points
        - Points positioned at (cos(phase), sin(phase))
        - Figure is interactive (zoom, pan, hover)
        - Resonance index displayed in title or annotation
    """
    # Convert phases to (x, y) coordinates
    x_coords = np.cos(phases)
    y_coords = np.sin(phases)

    # Create scatter plot for oscillators
    scatter = go.Scatter(
        x=x_coords,
        y=y_coords,
        mode="markers",
        marker=dict(
            size=8,
            color="blue",
            opacity=0.7,
            line=dict(width=1, color="darkblue"),
        ),
        name="Oscillators",
        hovertemplate="Phase: %{text}<br>X: %{x:.3f}<br>Y: %{y:.3f}<extra></extra>",
        text=[f"{phase:.3f}" for phase in phases],
    )

    # Create unit circle outline
    theta_circle = np.linspace(0, 2 * np.pi, 100)
    circle_x = np.cos(theta_circle)
    circle_y = np.sin(theta_circle)

    circle_trace = go.Scatter(
        x=circle_x,
        y=circle_y,
        mode="lines",
        line=dict(color="gray", width=1, dash="dash"),
        name="Unit Circle",
        showlegend=False,
        hoverinfo="skip",
    )

    # Create figure
    fig = go.Figure(data=[circle_trace, scatter])

    # Update layout
    fig.update_layout(
        title=f"Unit Circle Visualization (Resonance Index: R = {resonance_index:.3f})",
        xaxis=dict(
            title="X (cos(θ))",
            range=[-1.2, 1.2],
            scaleanchor="y",
            scaleratio=1,
        ),
        yaxis=dict(
            title="Y (sin(θ))",
            range=[-1.2, 1.2],
        ),
        width=600,
        height=600,
        showlegend=True,
        hovermode="closest",
    )

    return fig

