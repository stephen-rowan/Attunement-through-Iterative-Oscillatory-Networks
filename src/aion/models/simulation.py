"""Simulation state and parameters for AION simulation."""

from dataclasses import dataclass
import numpy as np
from typing import Optional

from aion.models.oscillator import Oscillator


@dataclass
class SimulationParameters:
    """Immutable parameter container for simulation configuration."""

    num_oscillators: int  # [1, 1000]
    coupling_strength: float  # [0, 10]
    time_step: float  # (0, 1]
    frequency_range: tuple[float, float]  # (min, max), min < max
    animation_speed: float  # [0.1, 10.0]

    def __post_init__(self) -> None:
        """Validate parameters after initialization."""
        if not (1 <= self.num_oscillators <= 1000):
            raise ValueError(f"num_oscillators must be in [1, 1000], got {self.num_oscillators}")
        if not (0 <= self.coupling_strength <= 10):
            raise ValueError(f"coupling_strength must be in [0, 10], got {self.coupling_strength}")
        if not (0 < self.time_step <= 1):
            raise ValueError(f"time_step must be in (0, 1], got {self.time_step}")
        if not (self.frequency_range[0] < self.frequency_range[1]):
            raise ValueError(
                f"frequency_range min must be < max, got {self.frequency_range}"
            )
        if not all(np.isfinite(f) for f in self.frequency_range):
            raise ValueError(f"frequency_range values must be finite, got {self.frequency_range}")
        if not (0.1 <= self.animation_speed <= 10.0):
            raise ValueError(
                f"animation_speed must be in [0.1, 10.0], got {self.animation_speed}"
            )
        if not np.isfinite(self.coupling_strength):
            raise ValueError(f"coupling_strength must be finite, got {self.coupling_strength}")
        if not np.isfinite(self.time_step):
            raise ValueError(f"time_step must be finite, got {self.time_step}")
        if not np.isfinite(self.animation_speed):
            raise ValueError(f"animation_speed must be finite, got {self.animation_speed}")


@dataclass
class SimulationControlState:
    """State of simulation execution controls."""

    is_running: bool = True
    is_paused: bool = False

    def __post_init__(self) -> None:
        """Validate control state."""
        if self.is_running and self.is_paused:
            raise ValueError("is_running and is_paused cannot both be True")


class SimulationState:
    """Manages the state of all oscillators and simulation metadata."""

    def __init__(self, num_oscillators: int, frequency_range: tuple[float, float]) -> None:
        """
        Initialize simulation with N oscillators.

        Args:
            num_oscillators: Number of oscillators (N >= 1)
            frequency_range: (min_freq, max_freq) for random frequency distribution

        Raises:
            ValueError: If num_oscillators < 1 or invalid frequency_range
        """
        if num_oscillators < 1:
            raise ValueError(f"num_oscillators must be >= 1, got {num_oscillators}")
        if not (frequency_range[0] < frequency_range[1]):
            raise ValueError(
                f"frequency_range min must be < max, got {frequency_range}"
            )
        if not all(np.isfinite(f) for f in frequency_range):
            raise ValueError(f"frequency_range values must be finite, got {frequency_range}")

        self._num_oscillators = num_oscillators
        self._frequency_range = frequency_range
        self._time = 0.0
        self._oscillators: list[Oscillator] = []

        # Initialize oscillators with random phases and frequencies
        self._initialize_oscillators()

    def _initialize_oscillators(self) -> None:
        """Initialize oscillators with random phases and frequencies."""
        self._oscillators = []
        rng = np.random.default_rng()

        for _ in range(self._num_oscillators):
            phase = rng.uniform(0, 2 * np.pi)
            frequency = rng.uniform(self._frequency_range[0], self._frequency_range[1])
            self._oscillators.append(Oscillator(phase, frequency))

    @property
    def oscillators(self) -> list[Oscillator]:
        """Get list of all oscillators."""
        return self._oscillators.copy()

    @property
    def time(self) -> float:
        """Get current simulation time."""
        return self._time

    @property
    def resonance_index(self) -> float:
        """
        Get current resonance index R [0, 1].

        Calculated as: R = |(1/N) Σ e^(iθ_j)|
        """
        if len(self._oscillators) == 0:
            return 0.0

        # Calculate complex phases: e^(iθ_j)
        phases = np.array([osc.phase for osc in self._oscillators])
        complex_phases = np.exp(1j * phases)

        # Calculate order parameter: R = |(1/N) Σ e^(iθ_j)|
        R = np.abs(np.mean(complex_phases))

        # Ensure R is in [0, 1] (should always be, but clamp for safety)
        return float(np.clip(R, 0.0, 1.0))

    def update(self, coupling_strength: float, time_step: float) -> None:
        """
        Update all oscillator phases and recalculate resonance index.

        Uses NumPy vectorization for efficient O(N²) all-to-all coupling calculation.

        Args:
            coupling_strength: K (coupling strength parameter)
            time_step: Δt (time increment)

        Post-conditions:
            - All oscillator phases updated via Kuramoto equation
            - time incremented by time_step
            - resonance_index recalculated
        """
        if not np.isfinite(coupling_strength) or coupling_strength < 0:
            raise ValueError(f"coupling_strength must be finite and >= 0, got {coupling_strength}")
        if not (time_step > 0 and np.isfinite(time_step)):
            raise ValueError(f"time_step must be positive and finite, got {time_step}")

        N = len(self._oscillators)
        if N == 0:
            return

        # Extract phases as NumPy array for vectorized operations
        phases = np.array([osc.phase for osc in self._oscillators])

        # Calculate coupling term for each oscillator using vectorized operations
        # For oscillator j: coupling_term = (K/N) Σ sin(θ_k - θ_j)
        # We compute all pairwise phase differences efficiently
        for i, oscillator in enumerate(self._oscillators):
            # Calculate phase differences: θ_k - θ_j for all k
            phase_diffs = phases - phases[i]

            # Calculate sin(θ_k - θ_j) for all k
            sin_diffs = np.sin(phase_diffs)

            # Sum over all k (all-to-all coupling)
            coupling_sum = np.sum(sin_diffs)

            # Calculate coupling term: (K/N) * sum
            coupling_term = (coupling_strength / N) * coupling_sum if N > 0 else 0.0

            # Update oscillator phase
            oscillator.update_phase(coupling_term, time_step)

        # Increment simulation time
        self._time += time_step

    def reset(self, frequency_range: tuple[float, float]) -> None:
        """
        Reset simulation to initial state with new random values.

        Args:
            frequency_range: (min_freq, max_freq) for reinitialization

        Post-conditions:
            - All oscillators reinitialized with random phases/frequencies
            - time = 0.0
            - resonance_index = 0.0
        """
        if not (frequency_range[0] < frequency_range[1]):
            raise ValueError(
                f"frequency_range min must be < max, got {frequency_range}"
            )
        if not all(np.isfinite(f) for f in frequency_range):
            raise ValueError(f"frequency_range values must be finite, got {frequency_range}")

        self._frequency_range = frequency_range
        self._time = 0.0
        self._initialize_oscillators()

