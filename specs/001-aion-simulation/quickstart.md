# Quickstart Guide: AION Educational Simulation

**Date**: 2025-01-27  
**Feature**: 001-aion-simulation

## Overview

This guide provides a quick start for developers implementing the AION educational simulation. It covers setup, key concepts, and implementation order.

## Prerequisites

- Python 3.11+ installed
- Basic familiarity with:
  - Python programming
  - Streamlit framework
  - NumPy for numerical computations
  - Plotly for visualizations

## Setup

### 1. Create Project Structure

```bash
# From repository root
mkdir -p src/aion/{models,visualization,ui}
mkdir -p tests/{unit,integration}
touch src/aion/__init__.py
touch src/aion/models/__init__.py
touch src/aion/visualization/__init__.py
touch src/aion/ui/__init__.py
touch src/app.py
touch src/config.py
touch requirements.txt
```

### 2. Install Dependencies

Create `requirements.txt`:
```txt
streamlit>=1.28.0
plotly>=5.17.0
numpy>=1.24.0
pytest>=7.4.0
pytest-cov>=4.1.0
```

Install:
```bash
pip install -r requirements.txt
```

### 3. Default Configuration

Create `src/config.py` with default parameters:
```python
DEFAULT_NUM_OSCILLATORS = 20
DEFAULT_COUPLING_STRENGTH = 2.0
DEFAULT_TIME_STEP = 0.01
DEFAULT_FREQUENCY_RANGE = (-1.0, 1.0)
DEFAULT_ANIMATION_SPEED = 1.0
```

## Implementation Order

### Phase 1: Core Models (Foundation)

1. **`src/aion/models/oscillator.py`**
   - Implement `Oscillator` class
   - Phase and frequency properties
   - Phase update logic (Kuramoto equation component)
   - Validation and edge cases

2. **`src/aion/models/simulation.py`**
   - Implement `SimulationState` class
   - Oscillator collection management
   - Kuramoto equation implementation (all-to-all coupling)
   - Resonance index calculation: R = |(1/N) Σ e^(iθ_j)|
   - Update and reset methods

3. **Unit Tests** (`tests/unit/`)
   - `test_oscillator.py`: Test phase updates, validation
   - `test_simulation.py`: Test Kuramoto dynamics, resonance calculation
   - Verify edge cases: K=0, N=1, etc.

### Phase 2: Visualization

4. **`src/aion/visualization/unit_circle.py`**
   - Implement `create_unit_circle_plot()`
   - Convert phases to (x, y) coordinates: (cos(θ), sin(θ))
   - Create Plotly scatter plot on unit circle
   - Add resonance index to title/annotation

5. **`src/aion/visualization/resonance_chart.py`**
   - Implement `create_resonance_chart()`
   - Create Plotly line chart
   - X-axis: time, Y-axis: resonance_index [0, 1]
   - Handle time series data efficiently

### Phase 3: UI Components

6. **`src/aion/ui/controls.py`**
   - Implement `render_parameter_controls()` using Streamlit sliders
   - Implement `render_simulation_controls()` with pause/resume/reset buttons
   - Parameter validation and range checking

7. **`src/aion/ui/education.py`**
   - Implement `render_educational_content()`
   - Define explanations for: oscillator, phase, resonance, attunement
   - Connect to broader concepts (synchronization, energy minimization, neuro-symbolic binding)
   - Use `st.expander()` or sidebar for collapsible content

### Phase 4: Main Application

8. **`src/app.py`**
   - Streamlit entry point
   - Initialize session state for simulation state and parameters
   - Layout: sidebar for controls, main area for visualizations
   - Simulation loop:
     - Check if running and not paused
     - Update simulation state
     - Update visualizations
     - Handle parameter changes
     - Handle control actions (pause/resume/reset)

9. **Integration Tests** (`tests/integration/`)
   - Test full simulation flow
   - Test parameter changes
   - Test pause/resume/reset functionality

## Key Implementation Details

### Kuramoto Equation

The phase update for oscillator j:
```
dθ_j/dt = ω_j + (K/N) Σ sin(θ_k - θ_j)
```

Discretized with Euler method:
```
θ_j(t+Δt) = θ_j(t) + Δt * [ω_j + (K/N) Σ sin(θ_k - θ_j)]
```

**Implementation tip**: Use NumPy vectorization for efficient all-to-all coupling calculation.

### Resonance Index

```
R = |(1/N) Σ e^(iθ_j)|
```

**Implementation tip**: Use NumPy's complex number support:
```python
import numpy as np
complex_phases = np.exp(1j * phases)
R = np.abs(np.mean(complex_phases))
```

### Streamlit Session State

Use session state to persist simulation state across reruns:
```python
if 'simulation_state' not in st.session_state:
    st.session_state.simulation_state = SimulationState(...)
```

### Real-time Updates

Use `st.empty()` containers for efficient plot updates:
```python
plot_container = st.empty()
# In update loop:
with plot_container.container():
    fig = create_unit_circle_plot(...)
    st.plotly_chart(fig, use_container_width=True)
```

## Testing Strategy

1. **Unit Tests**: Test core logic independently
   - Oscillator phase updates
   - Kuramoto equation correctness
   - Resonance index calculation
   - Edge cases (K=0, N=1, etc.)

2. **Integration Tests**: Test Streamlit app flow
   - Mock Streamlit components or use `streamlit.testing`
   - Verify parameter changes affect simulation
   - Test control actions

## Running the Application

```bash
# From repository root
streamlit run src/app.py
```

The application will open in your default web browser at `http://localhost:8501`.

## Common Pitfalls

1. **Phase Wrapping**: Ensure phases stay in [0, 2π) range after updates
   ```python
   phase = phase % (2 * np.pi)
   ```

2. **Performance**: For large N, consider optimizing the O(N²) coupling calculation
   - NumPy vectorization is essential
   - Consider limiting resonance history size

3. **Streamlit Reruns**: Understand Streamlit's execution model
   - Script reruns on user interaction
   - Use session state to persist simulation state
   - Avoid expensive computations in every rerun

4. **Numerical Stability**: Very high coupling strength (K) may cause instability
   - Consider adaptive time stepping or validation

## Next Steps

After implementation:
1. Run all tests: `pytest tests/`
2. Test the application manually with various parameters
3. Verify all acceptance scenarios from spec.md
4. Check performance goals (10+ fps, <1s response time)

## References

- **Specification**: [spec.md](./spec.md)
- **Data Model**: [data-model.md](./data-model.md)
- **Module Contracts**: [contracts/module-interfaces.md](./contracts/module-interfaces.md)
- **Research**: [research.md](./research.md)

