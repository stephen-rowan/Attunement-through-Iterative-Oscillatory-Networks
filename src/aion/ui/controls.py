"""UI controls for AION simulation."""

import streamlit as st
from aion.models.simulation import SimulationParameters, SimulationControlState


def render_parameter_controls(
    current_params: SimulationParameters,
) -> SimulationParameters:
    """
    Render Streamlit controls for simulation parameters.

    Args:
        current_params: Current parameter values

    Returns:
        Updated SimulationParameters from user input

    Contract:
        - Uses st.slider() for numeric parameters
        - Validates input ranges
        - Returns new parameters object (immutable update)
        - Handles invalid inputs gracefully
    """
    st.sidebar.header("Simulation Parameters")

    num_oscillators = st.sidebar.slider(
        "Number of Oscillators (N)",
        min_value=1,
        max_value=1000,
        value=current_params.num_oscillators,
        step=1,
        help="Number of oscillators in the network",
    )

    coupling_strength = st.sidebar.slider(
        "Coupling Strength (K)",
        min_value=0.0,
        max_value=10.0,
        value=current_params.coupling_strength,
        step=0.1,
        help="Strength of coupling between oscillators",
    )

    time_step = st.sidebar.slider(
        "Time Step (Δt)",
        min_value=0.001,
        max_value=1.0,
        value=current_params.time_step,
        step=0.001,
        format="%.3f",
        help="Simulation time increment",
    )

    animation_speed = st.sidebar.slider(
        "Animation Speed",
        min_value=0.1,
        max_value=10.0,
        value=current_params.animation_speed,
        step=0.1,
        help="Visual update rate multiplier",
    )

    # Frequency range (using two sliders)
    st.sidebar.subheader("Frequency Range")
    freq_min = st.sidebar.slider(
        "Min Frequency",
        min_value=-5.0,
        max_value=5.0,
        value=current_params.frequency_range[0],
        step=0.1,
        help="Minimum intrinsic frequency",
    )
    freq_max = st.sidebar.slider(
        "Max Frequency",
        min_value=-5.0,
        max_value=5.0,
        value=current_params.frequency_range[1],
        step=0.1,
        help="Maximum intrinsic frequency",
    )

    # Validate frequency range
    if freq_min >= freq_max:
        st.sidebar.error("Min frequency must be less than max frequency")
        # Return current params if invalid
        return current_params

    # Create new parameters object
    try:
        new_params = SimulationParameters(
            num_oscillators=num_oscillators,
            coupling_strength=coupling_strength,
            time_step=time_step,
            frequency_range=(freq_min, freq_max),
            animation_speed=animation_speed,
        )
        return new_params
    except ValueError as e:
        st.sidebar.error(f"Invalid parameters: {e}")
        return current_params


def render_simulation_controls(
    is_running: bool,
    is_paused: bool,
) -> tuple[bool, bool, bool]:
    """
    Render pause/resume/reset buttons.

    Args:
        is_running: Current running state
        is_paused: Current paused state

    Returns:
        (should_pause, should_resume, should_reset) tuple

    Contract:
        - Returns (True, False, False) if pause clicked
        - Returns (False, True, False) if resume clicked
        - Returns (False, False, True) if reset clicked
        - Returns (False, False, False) if no action
    """
    st.sidebar.header("Simulation Controls")

    should_pause = False
    should_resume = False
    should_reset = False

    col1, col2 = st.sidebar.columns(2)

    if is_running and not is_paused:
        # Show pause button
        if col1.button("⏸️ Pause", use_container_width=True):
            should_pause = True
    elif is_paused:
        # Show resume button
        if col1.button("▶️ Resume", use_container_width=True):
            should_resume = True

    # Reset button (always available)
    if col2.button("🔄 Reset", use_container_width=True):
        should_reset = True

    return (should_pause, should_resume, should_reset)

