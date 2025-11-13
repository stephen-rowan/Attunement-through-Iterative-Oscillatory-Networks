"""Visualization components for AION simulation."""

from dataclasses import dataclass
from typing import Optional
import numpy as np


@dataclass
class VisualizationData:
    """Data structure for visualization rendering."""

    unit_circle_data: dict[str, list[float]]  # {"x": [...], "y": [...], "phases": [...]}
    resonance_history: list[tuple[float, float]]  # [(time, R), ...]

    @classmethod
    def from_simulation_state(
        cls,
        simulation_state,
        resonance_history: Optional[list[tuple[float, float]]] = None,
    ) -> "VisualizationData":
        """
        Create VisualizationData from SimulationState.

        Args:
            simulation_state: SimulationState instance
            resonance_history: Optional existing history to append to

        Returns:
            VisualizationData instance
        """
        phases = [osc.phase for osc in simulation_state.oscillators]
        x_coords = [float(np.cos(phase)) for phase in phases]
        y_coords = [float(np.sin(phase)) for phase in phases]

        unit_circle_data = {
            "x": x_coords,
            "y": y_coords,
            "phases": phases,
        }

        # Append current state to history
        if resonance_history is None:
            resonance_history = []

        current_point = (simulation_state.time, simulation_state.resonance_index)
        resonance_history = resonance_history + [current_point]

        # Limit history size for performance (keep last 1000 points)
        MAX_HISTORY_SIZE = 1000
        if len(resonance_history) > MAX_HISTORY_SIZE:
            resonance_history = resonance_history[-MAX_HISTORY_SIZE:]

        return cls(
            unit_circle_data=unit_circle_data,
            resonance_history=resonance_history,
        )


# Import visualization functions
from aion.visualization.unit_circle import create_unit_circle_plot
from aion.visualization.resonance_chart import create_resonance_chart
