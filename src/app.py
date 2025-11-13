"""Main Streamlit application for AION educational simulation."""

import streamlit as st
import time
import sys
from pathlib import Path

# Add src directory to path for imports when running as script
if Path(__file__).parent.name == "src":
    sys.path.insert(0, str(Path(__file__).parent.parent))

from config import (
    DEFAULT_NUM_OSCILLATORS,
    DEFAULT_COUPLING_STRENGTH,
    DEFAULT_TIME_STEP,
    DEFAULT_FREQUENCY_RANGE,
    DEFAULT_ANIMATION_SPEED,
)
from aion.models.simulation import (
    SimulationState,
    SimulationParameters,
    SimulationControlState,
)
from aion.visualization import (
    VisualizationData,
    create_unit_circle_plot,
    create_resonance_chart,
)
from aion.ui.controls import render_parameter_controls, render_simulation_controls
from aion.ui.education import render_educational_content


def initialize_session_state():
    """Initialize Streamlit session state with default values."""
    if "simulation_state" not in st.session_state:
        st.session_state.simulation_state = SimulationState(
            num_oscillators=DEFAULT_NUM_OSCILLATORS,
            frequency_range=DEFAULT_FREQUENCY_RANGE,
        )

    if "simulation_parameters" not in st.session_state:
        st.session_state.simulation_parameters = SimulationParameters(
            num_oscillators=DEFAULT_NUM_OSCILLATORS,
            coupling_strength=DEFAULT_COUPLING_STRENGTH,
            time_step=DEFAULT_TIME_STEP,
            frequency_range=DEFAULT_FREQUENCY_RANGE,
            animation_speed=DEFAULT_ANIMATION_SPEED,
        )

    if "control_state" not in st.session_state:
        st.session_state.control_state = SimulationControlState(
            is_running=True,
            is_paused=False,
        )

    if "visualization_data" not in st.session_state:
        st.session_state.visualization_data = VisualizationData.from_simulation_state(
            st.session_state.simulation_state
        )


def handle_parameter_changes():
    """Handle parameter changes from UI controls with error handling."""
    try:
        new_params = render_parameter_controls(st.session_state.simulation_parameters)

        # Check if num_oscillators changed (requires reinitialization)
        if new_params.num_oscillators != st.session_state.simulation_parameters.num_oscillators:
            try:
                # Reinitialize simulation with new N
                st.session_state.simulation_state = SimulationState(
                    num_oscillators=new_params.num_oscillators,
                    frequency_range=new_params.frequency_range,
                )
                # Reset visualization history
                st.session_state.visualization_data = VisualizationData.from_simulation_state(
                    st.session_state.simulation_state
                )
            except (ValueError, TypeError) as e:
                st.error(f"Error reinitializing simulation: {e}")
                return  # Keep old parameters

        # Check if frequency_range changed (requires reset)
        if new_params.frequency_range != st.session_state.simulation_parameters.frequency_range:
            try:
                st.session_state.simulation_state.reset(new_params.frequency_range)
                # Reset visualization history
                st.session_state.visualization_data = VisualizationData.from_simulation_state(
                    st.session_state.simulation_state
                )
            except (ValueError, TypeError) as e:
                st.error(f"Error resetting simulation: {e}")
                return  # Keep old parameters

        # Update parameters
        st.session_state.simulation_parameters = new_params
    except Exception as e:
        st.error(f"Error handling parameter changes: {e}")


def handle_control_actions():
    """Handle simulation control actions (pause/resume/reset)."""
    should_pause, should_resume, should_reset = render_simulation_controls(
        st.session_state.control_state.is_running,
        st.session_state.control_state.is_paused,
    )

    if should_pause:
        st.session_state.control_state.is_running = False
        st.session_state.control_state.is_paused = True

    if should_resume:
        st.session_state.control_state.is_running = True
        st.session_state.control_state.is_paused = False
        # Apply any parameter changes made during pause
        handle_parameter_changes()

    if should_reset:
        st.session_state.simulation_state.reset(
            st.session_state.simulation_parameters.frequency_range
        )
        # Clear resonance history
        st.session_state.visualization_data = VisualizationData.from_simulation_state(
            st.session_state.simulation_state
        )
        # Reset control state to running
        st.session_state.control_state.is_running = True
        st.session_state.control_state.is_paused = False


def update_simulation():
    """Update simulation state if running and not paused, with error handling."""
    if st.session_state.control_state.is_running and not st.session_state.control_state.is_paused:
        try:
            st.session_state.simulation_state.update(
                coupling_strength=st.session_state.simulation_parameters.coupling_strength,
                time_step=st.session_state.simulation_parameters.time_step,
            )

            # Update visualization data
            st.session_state.visualization_data = VisualizationData.from_simulation_state(
                st.session_state.simulation_state,
                resonance_history=st.session_state.visualization_data.resonance_history,
            )
        except (ValueError, TypeError) as e:
            st.error(f"Error updating simulation: {e}")
            # Pause simulation on error to prevent repeated errors
            st.session_state.control_state.is_running = False
            st.session_state.control_state.is_paused = True
        except Exception as e:
            st.error(f"Unexpected error in simulation update: {e}")
            st.session_state.control_state.is_running = False
            st.session_state.control_state.is_paused = True


def render_visualizations(unit_circle_container, resonance_container):
    """Render unit circle plot and resonance chart using containers for smooth updates."""
    # Get fresh data from simulation state (don't rely on cached visualization_data)
    phases = [osc.phase for osc in st.session_state.simulation_state.oscillators]
    resonance_index = st.session_state.simulation_state.resonance_index
    resonance_history = st.session_state.visualization_data.resonance_history

    # Use container context manager for smoother updates (reduces flickering)
    with unit_circle_container.container():
        unit_circle_fig = create_unit_circle_plot(
            phases=phases,
            resonance_index=resonance_index,
        )
        st.plotly_chart(unit_circle_fig, width='stretch', key="unit_circle")

    with resonance_container.container():
        resonance_fig = create_resonance_chart(resonance_history)
        st.plotly_chart(resonance_fig, width='stretch', key="resonance_chart")


def main():
    """Main Streamlit application entry point."""
    st.set_page_config(
        page_title="AION Educational Simulation",
        page_icon="🌀",
        layout="wide",
    )

    st.title("🌀 AION Educational Simulation")
    st.markdown(
        "**Attunement through Iterative Oscillatory Networks** - "
        "Watch oscillators synchronize through phase coupling"
    )

    # Initialize session state
    initialize_session_state()

    # Render educational content
    render_educational_content()

    # Handle parameter changes (if not paused, changes apply immediately)
    if not st.session_state.control_state.is_paused:
        handle_parameter_changes()
    else:
        # Still render controls but don't apply changes until resume
        render_parameter_controls(st.session_state.simulation_parameters)

    # Handle control actions
    handle_control_actions()

    # Main content area
    col1, col2 = st.columns([2, 1])

    with col1:
        st.header("Visualizations")
        
        # Create empty containers for smooth plot updates (persist across reruns)
        if "unit_circle_container" not in st.session_state:
            st.session_state.unit_circle_container = st.empty()
        if "resonance_container" not in st.session_state:
            st.session_state.resonance_container = st.empty()

        # Update simulation (batch updates for smoother animation)
        # Larger batches = fewer reruns = less flickering
        if st.session_state.control_state.is_running and not st.session_state.control_state.is_paused:
            # Batch multiple simulation steps before rendering to reduce flickering
            # With time_step=0.01, running 10 steps = 0.1 time units per render
            batch_size = 10  # Increased batch size to reduce rerun frequency
            for _ in range(batch_size):
                update_simulation()

        # Render visualizations using containers for smooth updates
        render_visualizations(
            st.session_state.unit_circle_container,
            st.session_state.resonance_container
        )

    with col2:
        st.header("Simulation Info")
        st.metric("Resonance Index", f"{st.session_state.simulation_state.resonance_index:.3f}")
        st.metric("Time", f"{st.session_state.simulation_state.time:.2f}")
        st.metric("Oscillators", st.session_state.simulation_parameters.num_oscillators)

        st.subheader("Current Parameters")
        st.write(f"**Coupling Strength (K):** {st.session_state.simulation_parameters.coupling_strength:.2f}")
        st.write(f"**Time Step (Δt):** {st.session_state.simulation_parameters.time_step:.3f}")
        st.write(f"**Animation Speed:** {st.session_state.simulation_parameters.animation_speed:.1f}x")

    # Auto-refresh for real-time updates
    # Slower updates = less flickering
    if st.session_state.control_state.is_running and not st.session_state.control_state.is_paused:
        # Use slower update rate to minimize flickering
        max_animation_speed = 1.5  # Reduced max speed to prevent flickering
        animation_speed = min(
            st.session_state.simulation_parameters.animation_speed,
            max_animation_speed
        )
        
        # Slower base refresh rate to reduce flickering (1-2 fps)
        base_sleep = 0.6  # Base refresh rate (1.7 fps) - slower = smoother
        sleep_time = max(base_sleep / animation_speed, 0.3)  # Minimum 0.3s (3.3 fps max)
        
        # Sleep and then rerun (longer sleep = less flickering)
        time.sleep(sleep_time)
        st.rerun()


if __name__ == "__main__":
    main()

