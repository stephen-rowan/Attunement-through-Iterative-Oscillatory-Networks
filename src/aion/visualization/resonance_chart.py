"""Resonance index chart visualization for AION simulation."""

import plotly.graph_objects as go


def create_resonance_chart(
    resonance_history: list[tuple[float, float]],
) -> go.Figure:
    """
    Create Plotly line chart for resonance index over time.

    Args:
        resonance_history: List of (time, R) tuples

    Returns:
        Plotly Figure object ready for st.plotly_chart()

    Contract:
        - X-axis: time
        - Y-axis: resonance_index [0, 1]
        - Line chart with smooth updates
        - Interactive (zoom, pan, hover)
    """
    if not resonance_history:
        # Return empty chart if no data
        fig = go.Figure()
        fig.update_layout(
            title="Resonance Index Over Time",
            xaxis=dict(title="Time"),
            yaxis=dict(title="Resonance Index (R)", range=[0, 1]),
            width=800,
            height=400,
        )
        return fig

    # Extract time and resonance values
    times = [t for t, _ in resonance_history]
    resonance_values = [r for _, r in resonance_history]

    # Create line chart
    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=times,
            y=resonance_values,
            mode="lines",
            name="Resonance Index",
            line=dict(color="green", width=2),
            hovertemplate="Time: %{x:.3f}<br>R: %{y:.3f}<extra></extra>",
        )
    )

    # Update layout
    fig.update_layout(
        title="Resonance Index Over Time",
        xaxis=dict(title="Time"),
        yaxis=dict(title="Resonance Index (R)", range=[0, 1]),
        width=800,
        height=400,
        showlegend=True,
        hovermode="x unified",
    )

    return fig

