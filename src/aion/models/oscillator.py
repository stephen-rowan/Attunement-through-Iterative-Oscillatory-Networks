"""Oscillator model for AION simulation."""

import numpy as np


class Oscillator:
    """Represents a single oscillator in the AION network."""

    def __init__(self, phase: float, intrinsic_frequency: float) -> None:
        """
        Initialize oscillator with phase and frequency.

        Args:
            phase: Angular position [0, 2π)
            intrinsic_frequency: Natural rotation rate (finite float)

        Raises:
            ValueError: If phase not in [0, 2π) or frequency not finite
        """
        if not (0 <= phase < 2 * np.pi):
            raise ValueError(f"Phase must be in [0, 2π), got {phase}")
        if not np.isfinite(intrinsic_frequency):
            raise ValueError(f"Intrinsic frequency must be finite, got {intrinsic_frequency}")

        self._phase = phase
        self._intrinsic_frequency = intrinsic_frequency

    @property
    def phase(self) -> float:
        """Get current phase [0, 2π)."""
        return self._phase

    @property
    def intrinsic_frequency(self) -> float:
        """Get intrinsic frequency (immutable)."""
        return self._intrinsic_frequency

    def update_phase(self, coupling_term: float, time_step: float) -> None:
        """
        Update phase using Kuramoto equation.

        Args:
            coupling_term: (K/N) Σ sin(θ_k - θ_j) from all other oscillators
            time_step: Time increment Δt

        Post-condition: phase is in [0, 2π) range
        """
        if not np.isfinite(coupling_term):
            raise ValueError(f"Coupling term must be finite, got {coupling_term}")
        if not (time_step > 0 and np.isfinite(time_step)):
            raise ValueError(f"Time step must be positive and finite, got {time_step}")

        # Kuramoto equation: dθ_j/dt = ω_j + coupling_term
        # Discretized: θ_j(t+Δt) = θ_j(t) + Δt * (ω_j + coupling_term)
        new_phase = self._phase + time_step * (self._intrinsic_frequency + coupling_term)

        # Wrap phase to [0, 2π)
        self._phase = new_phase % (2 * np.pi)

