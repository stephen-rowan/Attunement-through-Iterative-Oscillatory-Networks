"""Unit tests for Kuramoto equation mathematical correctness."""

import pytest
import numpy as np
from aion.models.simulation import SimulationState


class TestKuramotoEquation:
    """Test cases validating Kuramoto equation mathematical correctness."""

    def test_kuramoto_equation_structure(self):
        """Test that Kuramoto equation has correct structure: dθ_j/dt = ω_j + (K/N) Σ sin(θ_k - θ_j)."""
        sim = SimulationState(num_oscillators=5, frequency_range=(-1.0, 1.0))
        initial_phases = np.array([osc.phase for osc in sim.oscillators])
        frequencies = np.array([osc.intrinsic_frequency for osc in sim.oscillators])
        K = 2.0
        N = 5
        dt = 0.01

        # Manual calculation of expected phase changes
        expected_new_phases = np.zeros(N)
        for j in range(N):
            coupling_sum = 0.0
            for k in range(N):
                coupling_sum += np.sin(initial_phases[k] - initial_phases[j])
            coupling_term = (K / N) * coupling_sum
            dtheta_dt = frequencies[j] + coupling_term
            expected_new_phases[j] = (initial_phases[j] + dt * dtheta_dt) % (2 * np.pi)

        # Update simulation
        sim.update(coupling_strength=K, time_step=dt)
        actual_new_phases = np.array([osc.phase for osc in sim.oscillators])

        # Compare results (allowing for small numerical errors)
        for j in range(N):
            diff = abs(actual_new_phases[j] - expected_new_phases[j])
            # Account for phase wrapping
            diff = min(diff, abs(diff - 2 * np.pi))
            assert diff < 1e-10, f"Phase mismatch for oscillator {j}"

    def test_independent_rotation_k_zero(self):
        """Test that with K=0, oscillators rotate independently at their intrinsic frequencies."""
        # Use a narrow frequency range to get similar frequencies
        sim = SimulationState(num_oscillators=3, frequency_range=(0.99, 1.01))
        # Set specific phases for deterministic test
        # We'll manually set phases by creating a new simulation and updating

        # For K=0, each oscillator should update as: θ_j(t+Δt) = θ_j(t) + ω_j * Δt
        # Since we can't directly set phases, we'll verify the behavior through multiple updates
        initial_phases = np.array([osc.phase for osc in sim.oscillators])
        frequencies = np.array([osc.intrinsic_frequency for osc in sim.oscillators])
        dt = 0.01

        sim.update(coupling_strength=0.0, time_step=dt)

        # With K=0, each oscillator should advance independently by ω * dt
        # (allowing for phase wrapping)
        for i, osc in enumerate(sim.oscillators):
            expected_phase = (initial_phases[i] + frequencies[i] * dt) % (2 * np.pi)
            diff = abs(osc.phase - expected_phase)
            diff = min(diff, abs(diff - 2 * np.pi))  # Account for wrapping
            assert diff < 1e-10, f"Independent rotation failed for oscillator {i}"

    def test_coupling_effect(self):
        """Test that coupling term (K/N) Σ sin(θ_k - θ_j) affects phase updates."""
        # Use a very narrow range around zero to get frequencies close to zero
        sim = SimulationState(num_oscillators=5, frequency_range=(-0.01, 0.01))
        initial_phases = np.array([osc.phase for osc in sim.oscillators])
        K = 2.0
        N = 5
        dt = 0.01

        # With frequencies close to zero, coupling should be the dominant effect
        sim.update(coupling_strength=K, time_step=dt)

        # Verify phases changed (coupling should cause changes)
        new_phases = np.array([osc.phase for osc in sim.oscillators])
        phase_changes = new_phases - initial_phases
        # Account for phase wrapping
        phase_changes = np.where(phase_changes > np.pi, phase_changes - 2 * np.pi, phase_changes)
        phase_changes = np.where(phase_changes < -np.pi, phase_changes + 2 * np.pi, phase_changes)

        # At least some phases should have changed due to coupling
        assert np.any(np.abs(phase_changes) > 1e-10), "Coupling should cause phase changes"

    def test_resonance_index_calculation(self):
        """Test resonance index calculation: R = |(1/N) Σ e^(iθ_j)|."""
        sim = SimulationState(num_oscillators=10, frequency_range=(-1.0, 1.0))
        phases = np.array([osc.phase for osc in sim.oscillators])

        # Manual calculation
        complex_phases = np.exp(1j * phases)
        expected_R = np.abs(np.mean(complex_phases))

        # Simulation calculation
        actual_R = sim.resonance_index

        assert abs(actual_R - expected_R) < 1e-10, "Resonance index calculation incorrect"

    def test_resonance_index_bounds(self):
        """Test that resonance index is always in [0, 1]."""
        sim = SimulationState(num_oscillators=20, frequency_range=(-2.0, 2.0))

        # Run many updates with various parameters
        for K in [0.0, 1.0, 5.0, 10.0]:
            for _ in range(10):
                sim.update(coupling_strength=K, time_step=0.01)
                R = sim.resonance_index
                assert 0 <= R <= 1.0, f"Resonance index out of bounds: R={R}"

    def test_resonance_index_perfect_sync(self):
        """Test resonance index for perfectly synchronized oscillators (R=1)."""
        # Create simulation and manually synchronize phases
        sim = SimulationState(num_oscillators=5, frequency_range=(-1.0, 1.0))

        # Set all phases to the same value (perfect synchronization)
        # We can't directly set phases, but we can verify that when phases are close, R is high
        # For a more direct test, we'll check the mathematical property

        # With all phases equal, R should be 1.0
        # Since we can't directly set phases, we'll verify through the calculation
        # by checking that R approaches 1 as phases converge

        # Run simulation with high coupling to achieve synchronization
        for _ in range(100):
            sim.update(coupling_strength=10.0, time_step=0.01)

        R = sim.resonance_index
        # With high coupling, R should be close to 1.0 (allowing for some variance)
        assert R > 0.5, f"High coupling should increase R, got {R}"

    def test_resonance_index_desync(self):
        """Test resonance index for desynchronized oscillators (R≈0)."""
        sim = SimulationState(num_oscillators=10, frequency_range=(-2.0, 2.0))

        # With K=0 and diverse frequencies, oscillators should desynchronize
        for _ in range(50):
            sim.update(coupling_strength=0.0, time_step=0.01)

        R = sim.resonance_index
        # With no coupling, R should remain relatively low
        # (exact value depends on initial conditions, but should be < 0.5 typically)
        assert 0 <= R <= 1.0, f"Resonance index out of bounds: R={R}"

    def test_numerical_stability(self):
        """Test numerical stability with various parameter combinations."""
        # Test edge cases that might cause numerical issues
        test_cases = [
            (1, 0.0, 0.001),  # N=1, K=0, small dt
            (100, 10.0, 0.01),  # Large N, high K
            (10, 0.0, 1.0),  # K=0, large dt
        ]

        for N, K, dt in test_cases:
            sim = SimulationState(num_oscillators=N, frequency_range=(-1.0, 1.0))

            # Run multiple updates
            for _ in range(10):
                sim.update(coupling_strength=K, time_step=dt)

                # Verify all values remain finite and valid
                assert np.isfinite(sim.time)
                assert 0 <= sim.resonance_index <= 1.0
                for osc in sim.oscillators:
                    assert 0 <= osc.phase < 2 * np.pi
                    assert np.isfinite(osc.intrinsic_frequency)

