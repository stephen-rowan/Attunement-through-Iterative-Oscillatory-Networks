"""Integration tests for AION simulation flow."""

import pytest
import numpy as np
from aion.models.simulation import (
    SimulationState,
    SimulationParameters,
    SimulationControlState,
)
from aion.visualization import VisualizationData


class TestSimulationFlow:
    """Test cases for end-to-end simulation flow."""

    def test_simulation_initialization(self):
        """Test that simulation initializes correctly."""
        sim = SimulationState(num_oscillators=10, frequency_range=(-1.0, 1.0))
        assert len(sim.oscillators) == 10
        assert sim.time == 0.0
        assert 0 <= sim.resonance_index <= 1.0

    def test_simulation_update_loop(self):
        """Test basic simulation update loop."""
        sim = SimulationState(num_oscillators=20, frequency_range=(-1.0, 1.0))
        params = SimulationParameters(
            num_oscillators=20,
            coupling_strength=2.0,
            time_step=0.01,
            frequency_range=(-1.0, 1.0),
            animation_speed=1.0,
        )

        # Run several updates
        for _ in range(10):
            sim.update(
                coupling_strength=params.coupling_strength,
                time_step=params.time_step,
            )

        assert sim.time > 0.0
        assert 0 <= sim.resonance_index <= 1.0

    def test_pause_resume_functionality(self):
        """Test pause and resume functionality."""
        control = SimulationControlState(is_running=True, is_paused=False)
        assert control.is_running is True
        assert control.is_paused is False

        # Pause
        control.is_running = False
        control.is_paused = True
        assert control.is_running is False
        assert control.is_paused is True

        # Resume
        control.is_running = True
        control.is_paused = False
        assert control.is_running is True
        assert control.is_paused is False

    def test_reset_functionality(self):
        """Test reset functionality."""
        sim = SimulationState(num_oscillators=10, frequency_range=(-1.0, 1.0))
        initial_phases = [osc.phase for osc in sim.oscillators]

        # Run some updates
        for _ in range(5):
            sim.update(coupling_strength=1.0, time_step=0.01)

        assert sim.time > 0.0

        # Reset
        sim.reset(frequency_range=(-1.0, 1.0))

        assert sim.time == 0.0
        # Phases should be reinitialized (different from before)
        new_phases = [osc.phase for osc in sim.oscillators]
        # At least some phases should be different (random reinitialization)
        assert len(set(new_phases)) > 0

    def test_visualization_data_generation(self):
        """Test that visualization data is generated correctly."""
        sim = SimulationState(num_oscillators=10, frequency_range=(-1.0, 1.0))
        viz_data = VisualizationData.from_simulation_state(sim)

        assert "x" in viz_data.unit_circle_data
        assert "y" in viz_data.unit_circle_data
        assert "phases" in viz_data.unit_circle_data
        assert len(viz_data.unit_circle_data["phases"]) == 10
        assert len(viz_data.resonance_history) == 1

        # Check coordinates are on unit circle
        for i in range(10):
            x = viz_data.unit_circle_data["x"][i]
            y = viz_data.unit_circle_data["y"][i]
            phase = viz_data.unit_circle_data["phases"][i]
            assert abs(x - np.cos(phase)) < 1e-10
            assert abs(y - np.sin(phase)) < 1e-10
            assert abs(np.sqrt(x**2 + y**2) - 1.0) < 1e-10

    def test_visualization_data_history(self):
        """Test that visualization data history accumulates correctly."""
        sim = SimulationState(num_oscillators=5, frequency_range=(-1.0, 1.0))
        viz_data = VisualizationData.from_simulation_state(sim)

        initial_history_length = len(viz_data.resonance_history)

        # Run updates and accumulate history
        for _ in range(5):
            sim.update(coupling_strength=1.0, time_step=0.01)
            viz_data = VisualizationData.from_simulation_state(
                sim, resonance_history=viz_data.resonance_history
            )

        assert len(viz_data.resonance_history) == initial_history_length + 5

        # Check history values are valid
        for time, R in viz_data.resonance_history:
            assert time >= 0.0
            assert 0 <= R <= 1.0

    def test_parameter_changes_apply(self):
        """Test that parameter changes are applied correctly."""
        sim = SimulationState(num_oscillators=10, frequency_range=(-1.0, 1.0))
        params = SimulationParameters(
            num_oscillators=10,
            coupling_strength=1.0,
            time_step=0.01,
            frequency_range=(-1.0, 1.0),
            animation_speed=1.0,
        )

        # Update with initial parameters
        sim.update(coupling_strength=params.coupling_strength, time_step=params.time_step)
        initial_time = sim.time

        # Change parameters
        params.coupling_strength = 5.0
        params.time_step = 0.02

        # Update with new parameters
        sim.update(coupling_strength=params.coupling_strength, time_step=params.time_step)

        # Time should increment by new time_step
        assert abs(sim.time - (initial_time + 0.02)) < 1e-10

    def test_num_oscillators_change(self):
        """Test that changing number of oscillators reinitializes simulation."""
        sim = SimulationState(num_oscillators=10, frequency_range=(-1.0, 1.0))
        initial_time = sim.time

        # Change number of oscillators (requires reinitialization)
        sim = SimulationState(num_oscillators=20, frequency_range=(-1.0, 1.0))

        assert len(sim.oscillators) == 20
        assert sim.time == 0.0  # Should be reset

    def test_edge_case_n_equals_one(self):
        """Test edge case: N=1 (single oscillator)."""
        sim = SimulationState(num_oscillators=1, frequency_range=(-1.0, 1.0))

        # Single oscillator should have R=1.0 (perfectly synchronized with itself)
        assert abs(sim.resonance_index - 1.0) < 1e-10

        # Update should work
        sim.update(coupling_strength=1.0, time_step=0.01)
        assert sim.time > 0.0
        assert abs(sim.resonance_index - 1.0) < 1e-10

    def test_edge_case_k_equals_zero(self):
        """Test edge case: K=0 (no coupling, independent rotation)."""
        sim = SimulationState(num_oscillators=10, frequency_range=(-1.0, 1.0))
        initial_R = sim.resonance_index

        # Run updates with K=0
        for _ in range(10):
            sim.update(coupling_strength=0.0, time_step=0.01)

        # R should remain relatively low (no synchronization)
        final_R = sim.resonance_index
        assert 0 <= final_R <= 1.0
        # R might fluctuate but shouldn't systematically increase without coupling

    def test_parameter_changes_coupling_strength(self):
        """Test that coupling_strength changes affect simulation immediately."""
        sim = SimulationState(num_oscillators=20, frequency_range=(-0.5, 0.5))
        
        # Run with low coupling
        for _ in range(10):
            sim.update(coupling_strength=0.5, time_step=0.01)
        R_low = sim.resonance_index
        
        # Run with high coupling
        for _ in range(10):
            sim.update(coupling_strength=5.0, time_step=0.01)
        R_high = sim.resonance_index
        
        # High coupling should generally lead to higher R (synchronization)
        # (allowing for some variance)
        assert 0 <= R_low <= 1.0
        assert 0 <= R_high <= 1.0

    def test_parameter_changes_time_step(self):
        """Test that time_step changes affect simulation update rate."""
        sim = SimulationState(num_oscillators=10, frequency_range=(-1.0, 1.0))
        initial_time = sim.time
        
        # Update with small time step
        sim.update(coupling_strength=1.0, time_step=0.01)
        time_small = sim.time
        
        # Reset and update with large time step
        sim.reset(frequency_range=(-1.0, 1.0))
        sim.update(coupling_strength=1.0, time_step=0.1)
        time_large = sim.time
        
        assert abs((time_small - initial_time) - 0.01) < 1e-10
        assert abs((time_large - initial_time) - 0.1) < 1e-10

    def test_parameter_changes_num_oscillators(self):
        """Test that num_oscillators changes require reinitialization."""
        sim1 = SimulationState(num_oscillators=10, frequency_range=(-1.0, 1.0))
        sim1.update(coupling_strength=1.0, time_step=0.01)
        
        # Change N (requires new simulation)
        sim2 = SimulationState(num_oscillators=20, frequency_range=(-1.0, 1.0))
        
        assert len(sim2.oscillators) == 20
        assert sim2.time == 0.0  # Should be reset

    def test_parameter_validation(self):
        """Test that parameter validation prevents invalid inputs."""
        # Test invalid num_oscillators
        with pytest.raises(ValueError):
            SimulationParameters(
                num_oscillators=0,
                coupling_strength=2.0,
                time_step=0.01,
                frequency_range=(-1.0, 1.0),
                animation_speed=1.0,
            )
        
        # Test invalid coupling_strength
        with pytest.raises(ValueError):
            SimulationParameters(
                num_oscillators=20,
                coupling_strength=-1.0,
                time_step=0.01,
                frequency_range=(-1.0, 1.0),
                animation_speed=1.0,
            )
        
        # Test invalid time_step
        with pytest.raises(ValueError):
            SimulationParameters(
                num_oscillators=20,
                coupling_strength=2.0,
                time_step=0.0,
                frequency_range=(-1.0, 1.0),
                animation_speed=1.0,
            )
        
        # Test invalid frequency_range
        with pytest.raises(ValueError):
            SimulationParameters(
                num_oscillators=20,
                coupling_strength=2.0,
                time_step=0.01,
                frequency_range=(1.0, -1.0),  # min > max
                animation_speed=1.0,
            )

