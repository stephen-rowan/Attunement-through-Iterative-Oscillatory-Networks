# Module Interface Contracts

**Date**: 2025-01-27  
**Feature**: 001-aion-simulation

## Overview

This document defines the interface contracts between modules in the AION simulation application. These contracts ensure consistent integration and testability.

## Core Models

### `aion.models.oscillator.Oscillator`

```python
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
    
    @property
    def phase(self) -> float:
        """Get current phase [0, 2π)."""
    
    @property
    def intrinsic_frequency(self) -> float:
        """Get intrinsic frequency (immutable)."""
    
    def update_phase(self, coupling_term: float, time_step: float) -> None:
        """
        Update phase using Kuramoto equation.
        
        Args:
            coupling_term: (K/N) Σ sin(θ_k - θ_j) from all other oscillators
            time_step: Time increment Δt
        
        Post-condition: phase is in [0, 2π) range
        """
```

### `aion.models.simulation.SimulationState`

```python
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
    
    @property
    def oscillators(self) -> list[Oscillator]:
        """Get list of all oscillators."""
    
    @property
    def time(self) -> float:
        """Get current simulation time."""
    
    @property
    def resonance_index(self) -> float:
        """Get current resonance index R [0, 1]."""
    
    def update(self, coupling_strength: float, time_step: float) -> None:
        """
        Update all oscillator phases and recalculate resonance index.
        
        Args:
            coupling_strength: K (coupling strength parameter)
            time_step: Δt (time increment)
        
        Post-conditions:
            - All oscillator phases updated via Kuramoto equation
            - time incremented by time_step
            - resonance_index recalculated
        """
    
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
```

## Visualization Modules

### `aion.visualization.unit_circle.create_unit_circle_plot`

```python
def create_unit_circle_plot(
    phases: list[float],
    resonance_index: float
) -> plotly.graph_objects.Figure:
    """
    Create Plotly figure for unit circle visualization.
    
    Args:
        phases: List of oscillator phases [0, 2π)
        resonance_index: Current R value for display
    
    Returns:
        Plotly Figure object ready for st.plotly_chart()
    
    Contract:
        - Figure shows unit circle with oscillators as points
        - Points positioned at (cos(phase), sin(phase))
        - Figure is interactive (zoom, pan, hover)
        - Resonance index displayed in title or annotation
    """
```

### `aion.visualization.resonance_chart.create_resonance_chart`

```python
def create_resonance_chart(
    resonance_history: list[tuple[float, float]]
) -> plotly.graph_objects.Figure:
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
```

## UI Modules

### `aion.ui.controls.render_parameter_controls`

```python
def render_parameter_controls(
    current_params: SimulationParameters
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
```

### `aion.ui.controls.render_simulation_controls`

```python
def render_simulation_controls(
    is_running: bool,
    is_paused: bool
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
```

### `aion.ui.education.render_educational_content`

```python
def render_educational_content() -> None:
    """
    Display educational explanations in Streamlit.
    
    Contract:
        - Shows definitions for: oscillator, phase, resonance, attunement
        - Explains connections to synchronization, energy minimization, neuro-symbolic binding
        - Uses st.expander() or st.sidebar() for collapsible content
        - Content is concise and accessible
    """
```

## Main Application

### `app.py` (Streamlit Entry Point)

```python
def main() -> None:
    """
    Main Streamlit application entry point.
    
    Contract:
        - Initializes session state if needed
        - Renders UI layout (sidebar for controls, main area for visualizations)
        - Manages simulation update loop
        - Handles parameter changes and control actions
        - Updates visualizations in real-time
    """
```

## Data Format Contracts

### SimulationParameters

```python
@dataclass
class SimulationParameters:
    """Immutable parameter container."""
    num_oscillators: int          # [1, 1000]
    coupling_strength: float      # [0, 10]
    time_step: float              # (0, 1]
    frequency_range: tuple[float, float]  # (min, max), min < max
    animation_speed: float        # [0.1, 10.0]
```

### VisualizationData

```python
@dataclass
class VisualizationData:
    """Data structure for visualization rendering."""
    unit_circle_data: dict[str, list[float]]  # {"x": [...], "y": [...], "phases": [...]}
    resonance_history: list[tuple[float, float]]  # [(time, R), ...]
```

## Error Handling Contracts

All modules must:
- Raise `ValueError` for invalid input parameters
- Raise `TypeError` for incorrect types
- Handle edge cases gracefully (e.g., N=1, K=0)
- Never raise unhandled exceptions that crash the Streamlit app

## Performance Contracts

- `SimulationState.update()` must complete in < 100ms for N=100 oscillators
- Visualization functions must return figures in < 50ms
- UI controls must respond to user input within 1 second

