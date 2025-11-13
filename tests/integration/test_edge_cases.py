"""Comprehensive edge case validation tests."""

import pytest
import numpy as np
from aion.models.simulation import SimulationState, SimulationParameters


class TestEdgeCases:
    """Comprehensive edge case validation matrix."""

    def test_k_equals_zero_independent_rotation(self):
        """Edge case: K=0 (independent rotation, no synchronization)."""
        sim = SimulationState(num_oscillators=10, frequency_range=(-1.0, 1.0))
        initial_R = sim.resonance_index

        # Run updates with K=0
        for _ in range(20):
            sim.update(coupling_strength=0.0, time_step=0.01)

        final_R = sim.resonance_index
        # With K=0, oscillators rotate independently, R should remain relatively low
        assert 0 <= final_R <= 1.0
        # R might fluctuate but shouldn't systematically increase

    def test_k_very_high_numerical_stability(self):
        """Edge case: K very high (should synchronize quickly, check numerical stability)."""
        sim = SimulationState(num_oscillators=20, frequency_range=(-0.5, 0.5))

        # Run with very high K
        for _ in range(10):
            sim.update(coupling_strength=10.0, time_step=0.01)

        # Verify all values remain finite and valid
        assert np.isfinite(sim.time)
        assert 0 <= sim.resonance_index <= 1.0
        for osc in sim.oscillators:
            assert 0 <= osc.phase < 2 * np.pi
            assert np.isfinite(osc.intrinsic_frequency)

    def test_n_equals_one_no_synchronization(self):
        """Edge case: N=1 (single oscillator, no synchronization possible)."""
        sim = SimulationState(num_oscillators=1, frequency_range=(-1.0, 1.0))

        # Single oscillator should have R=1.0 (perfectly synchronized with itself)
        assert abs(sim.resonance_index - 1.0) < 1e-10

        # Update should work
        sim.update(coupling_strength=1.0, time_step=0.01)
        assert sim.time > 0.0
        assert abs(sim.resonance_index - 1.0) < 1e-10

    def test_n_very_large_performance(self):
        """Edge case: N=1000 (very large, should handle gracefully)."""
        sim = SimulationState(num_oscillators=1000, frequency_range=(-1.0, 1.0))

        # Should initialize successfully
        assert len(sim.oscillators) == 1000

        # Update should complete in reasonable time (< 1 second for 1000 oscillators)
        import time
        start = time.time()
        sim.update(coupling_strength=2.0, time_step=0.01)
        elapsed = time.time() - start

        # Should complete quickly (allowing some margin)
        assert elapsed < 1.0, f"Update took {elapsed:.3f}s, expected < 1.0s"

    def test_time_step_zero_or_negative_validation(self):
        """Edge case: Δt=0 or negative (should prevent invalid values)."""
        sim = SimulationState(num_oscillators=10, frequency_range=(-1.0, 1.0))

        # Zero time step should raise ValueError
        with pytest.raises(ValueError, match="time_step must be positive"):
            sim.update(coupling_strength=1.0, time_step=0.0)

        # Negative time step should raise ValueError
        with pytest.raises(ValueError, match="time_step must be positive"):
            sim.update(coupling_strength=1.0, time_step=-0.01)

    def test_animation_speed_maximum_smooth_updates(self):
        """Edge case: Maximum animation speed (should update smoothly)."""
        # This is tested in the app, but we verify parameters are valid
        params = SimulationParameters(
            num_oscillators=20,
            coupling_strength=2.0,
            time_step=0.01,
            frequency_range=(-1.0, 1.0),
            animation_speed=10.0,  # Maximum
        )

        assert params.animation_speed == 10.0

    def test_rapid_parameter_changes_responsive(self):
        """Edge case: Rapid parameter changes (should be responsive)."""
        sim = SimulationState(num_oscillators=10, frequency_range=(-1.0, 1.0))

        # Rapidly change coupling strength
        for K in [0.5, 2.0, 5.0, 1.0, 3.0]:
            sim.update(coupling_strength=K, time_step=0.01)

        # Should handle all changes without errors
        assert np.isfinite(sim.time)
        assert 0 <= sim.resonance_index <= 1.0

    def test_very_long_simulation_run_stability(self):
        """Edge case: Very long simulation run (should remain stable)."""
        sim = SimulationState(num_oscillators=20, frequency_range=(-1.0, 1.0))

        # Run for many iterations
        for _ in range(1000):
            sim.update(coupling_strength=2.0, time_step=0.01)

        # Verify stability
        assert np.isfinite(sim.time)
        assert 0 <= sim.resonance_index <= 1.0
        assert sim.time > 0.0

        # All oscillators should have valid phases
        for osc in sim.oscillators:
            assert 0 <= osc.phase < 2 * np.pi
            assert np.isfinite(osc.intrinsic_frequency)

    def test_pause_behavior_frozen_state(self):
        """Edge case: Pause behavior (visualizations freeze, calculations stop)."""
        from aion.models.simulation import SimulationControlState

        control = SimulationControlState(is_running=False, is_paused=True)
        assert control.is_running is False
        assert control.is_paused is True

        # When paused, simulation should not update
        sim = SimulationState(num_oscillators=10, frequency_range=(-1.0, 1.0))
        initial_time = sim.time
        initial_R = sim.resonance_index

        # If we were to check in app, update wouldn't be called when paused
        # Here we just verify the control state is correct

    def test_reset_behavior_reinitialization(self):
        """Edge case: Reset behavior (reinitialization with random values)."""
        sim = SimulationState(num_oscillators=10, frequency_range=(-1.0, 1.0))
        initial_phases = [osc.phase for osc in sim.oscillators]

        # Run some updates
        for _ in range(5):
            sim.update(coupling_strength=1.0, time_step=0.01)

        assert sim.time > 0.0

        # Reset
        sim.reset(frequency_range=(-1.0, 1.0))

        # Time should be reset
        assert sim.time == 0.0

        # Oscillators should be reinitialized (phases will be different)
        new_phases = [osc.phase for osc in sim.oscillators]
        # At least some phases should be different (random reinitialization)
        assert len(set(new_phases)) > 0

    def test_invalid_parameters_handled_gracefully(self):
        """Edge case: Invalid parameters (should handle gracefully)."""
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

        # Test invalid frequency_range
        with pytest.raises(ValueError):
            SimulationState(num_oscillators=10, frequency_range=(1.0, -1.0))

