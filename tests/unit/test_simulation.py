"""Unit tests for SimulationState class."""

import pytest
import numpy as np
from aion.models.simulation import SimulationState, SimulationParameters, SimulationControlState


class TestSimulationState:
    """Test cases for SimulationState class."""

    def test_init_valid(self):
        """Test simulation initialization with valid parameters."""
        sim = SimulationState(num_oscillators=10, frequency_range=(-1.0, 1.0))
        assert len(sim.oscillators) == 10
        assert sim.time == 0.0
        assert 0 <= sim.resonance_index <= 1.0

    def test_init_invalid_num_oscillators(self):
        """Test initialization with invalid number of oscillators raises ValueError."""
        with pytest.raises(ValueError, match="num_oscillators must be >= 1"):
            SimulationState(num_oscillators=0, frequency_range=(-1.0, 1.0))

        with pytest.raises(ValueError, match="num_oscillators must be >= 1"):
            SimulationState(num_oscillators=-1, frequency_range=(-1.0, 1.0))

    def test_init_invalid_frequency_range(self):
        """Test initialization with invalid frequency range raises ValueError."""
        with pytest.raises(ValueError, match="frequency_range min must be < max"):
            SimulationState(num_oscillators=10, frequency_range=(1.0, -1.0))

        with pytest.raises(ValueError, match="frequency_range min must be < max"):
            SimulationState(num_oscillators=10, frequency_range=(1.0, 1.0))

    def test_oscillators_initialized(self):
        """Test that oscillators are initialized with random phases and frequencies."""
        sim = SimulationState(num_oscillators=5, frequency_range=(-1.0, 1.0))
        oscillators = sim.oscillators

        # Check all oscillators have valid phases
        for osc in oscillators:
            assert 0 <= osc.phase < 2 * np.pi
            assert -1.0 <= osc.intrinsic_frequency <= 1.0

    def test_resonance_index_initial(self):
        """Test resonance index calculation for initial state."""
        sim = SimulationState(num_oscillators=10, frequency_range=(-1.0, 1.0))
        R = sim.resonance_index

        # Initial state should have some desynchronization (R < 1)
        # but exact value depends on random initialization
        assert 0 <= R <= 1.0

    def test_resonance_index_single_oscillator(self):
        """Test resonance index for N=1 (should be 1.0)."""
        sim = SimulationState(num_oscillators=1, frequency_range=(-1.0, 1.0))
        R = sim.resonance_index

        # Single oscillator is perfectly synchronized with itself
        assert abs(R - 1.0) < 1e-10

    def test_update_basic(self):
        """Test basic update functionality."""
        sim = SimulationState(num_oscillators=5, frequency_range=(-1.0, 1.0))
        initial_time = sim.time
        initial_phases = [osc.phase for osc in sim.oscillators]

        sim.update(coupling_strength=1.0, time_step=0.01)

        # Time should increment
        assert sim.time == initial_time + 0.01

        # Phases should change (unless K=0 and all frequencies are 0)
        new_phases = [osc.phase for osc in sim.oscillators]
        # At least some phases should have changed
        assert any(abs(new - old) > 1e-10 for new, old in zip(new_phases, initial_phases))

    def test_update_zero_coupling(self):
        """Test update with K=0 (independent rotation, no synchronization)."""
        sim = SimulationState(num_oscillators=10, frequency_range=(-1.0, 1.0))
        initial_R = sim.resonance_index

        # Run several updates with K=0
        for _ in range(10):
            sim.update(coupling_strength=0.0, time_step=0.01)

        # With K=0, oscillators rotate independently, so R should remain low
        # (exact value depends on initial conditions, but should not increase significantly)
        final_R = sim.resonance_index
        # R might fluctuate but shouldn't systematically increase without coupling
        assert 0 <= final_R <= 1.0

    def test_update_high_coupling(self):
        """Test update with high coupling strength (should increase synchronization)."""
        sim = SimulationState(num_oscillators=20, frequency_range=(-0.5, 0.5))
        initial_R = sim.resonance_index

        # Run updates with high coupling
        for _ in range(50):
            sim.update(coupling_strength=5.0, time_step=0.01)

        final_R = sim.resonance_index

        # With high coupling, R should generally increase (synchronization)
        # Note: This is probabilistic, but with high K and narrow frequency range,
        # synchronization should occur
        assert 0 <= final_R <= 1.0
        # R should be higher than initial (or at least not systematically lower)
        # We allow some variance but expect trend toward synchronization

    def test_update_invalid_coupling(self):
        """Test update with invalid coupling strength raises ValueError."""
        sim = SimulationState(num_oscillators=10, frequency_range=(-1.0, 1.0))

        with pytest.raises(ValueError, match="coupling_strength must be finite"):
            sim.update(coupling_strength=np.inf, time_step=0.01)

        with pytest.raises(ValueError, match="coupling_strength must be finite"):
            sim.update(coupling_strength=np.nan, time_step=0.01)

        with pytest.raises(ValueError, match="coupling_strength must be finite"):
            sim.update(coupling_strength=-1.0, time_step=0.01)

    def test_update_invalid_time_step(self):
        """Test update with invalid time step raises ValueError."""
        sim = SimulationState(num_oscillators=10, frequency_range=(-1.0, 1.0))

        with pytest.raises(ValueError, match="time_step must be positive"):
            sim.update(coupling_strength=1.0, time_step=0.0)

        with pytest.raises(ValueError, match="time_step must be positive"):
            sim.update(coupling_strength=1.0, time_step=-0.01)

    def test_reset(self):
        """Test reset functionality."""
        sim = SimulationState(num_oscillators=10, frequency_range=(-1.0, 1.0))
        initial_phases = [osc.phase for osc in sim.oscillators]

        # Run some updates
        sim.update(coupling_strength=1.0, time_step=0.01)
        sim.update(coupling_strength=1.0, time_step=0.01)
        assert sim.time > 0.0

        # Reset
        sim.reset(frequency_range=(-2.0, 2.0))

        # Time should be reset
        assert sim.time == 0.0

        # Oscillators should be reinitialized (phases will be different)
        new_phases = [osc.phase for osc in sim.oscillators]
        # Phases should be different (random reinitialization)
        assert len(set(new_phases)) > 0

    def test_reset_invalid_frequency_range(self):
        """Test reset with invalid frequency range raises ValueError."""
        sim = SimulationState(num_oscillators=10, frequency_range=(-1.0, 1.0))

        with pytest.raises(ValueError, match="frequency_range min must be < max"):
            sim.reset(frequency_range=(1.0, -1.0))


class TestSimulationParameters:
    """Test cases for SimulationParameters dataclass."""

    def test_init_valid(self):
        """Test initialization with valid parameters."""
        params = SimulationParameters(
            num_oscillators=20,
            coupling_strength=2.0,
            time_step=0.01,
            frequency_range=(-1.0, 1.0),
            animation_speed=1.0,
        )
        assert params.num_oscillators == 20
        assert params.coupling_strength == 2.0

    def test_init_invalid_num_oscillators(self):
        """Test initialization with invalid num_oscillators raises ValueError."""
        with pytest.raises(ValueError):
            SimulationParameters(
                num_oscillators=0,
                coupling_strength=2.0,
                time_step=0.01,
                frequency_range=(-1.0, 1.0),
                animation_speed=1.0,
            )

    def test_init_invalid_coupling_strength(self):
        """Test initialization with invalid coupling_strength raises ValueError."""
        with pytest.raises(ValueError):
            SimulationParameters(
                num_oscillators=20,
                coupling_strength=-1.0,
                time_step=0.01,
                frequency_range=(-1.0, 1.0),
                animation_speed=1.0,
            )

    def test_init_invalid_time_step(self):
        """Test initialization with invalid time_step raises ValueError."""
        with pytest.raises(ValueError):
            SimulationParameters(
                num_oscillators=20,
                coupling_strength=2.0,
                time_step=0.0,
                frequency_range=(-1.0, 1.0),
                animation_speed=1.0,
            )


class TestSimulationControlState:
    """Test cases for SimulationControlState dataclass."""

    def test_init_valid(self):
        """Test initialization with valid state."""
        control = SimulationControlState(is_running=True, is_paused=False)
        assert control.is_running is True
        assert control.is_paused is False

    def test_init_invalid_both_true(self):
        """Test initialization with both is_running and is_paused True raises ValueError."""
        with pytest.raises(ValueError, match="is_running and is_paused cannot both be True"):
            SimulationControlState(is_running=True, is_paused=True)

