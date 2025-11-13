# Data Model: AION Educational Simulation

**Date**: 2025-01-27  
**Feature**: 001-aion-simulation

## Overview

The AION simulation implements a Kuramoto-style oscillator network where each oscillator has a phase and intrinsic frequency. The data model captures the state of oscillators, simulation parameters, and visualization data.

## Entities

### 1. Oscillator

Represents a single node in the AION network.

**Fields**:
- `phase` (float): Angular position on the unit circle, range [0, 2π)
  - Initialization: Random uniform distribution on [0, 2π)
  - Validation: Must be in [0, 2π) range
  - Updates: Modified by Kuramoto equation: dθ_j/dt = ω_j + (K/N) Σ sin(θ_k - θ_j)
  
- `intrinsic_frequency` (float): Natural rotation rate of the oscillator
  - Initialization: Random uniform distribution over a specified range (e.g., [-1, 1] or [0, 2])
  - Validation: Must be a finite real number
  - Immutability: Does not change during simulation (constant for each oscillator)

**Relationships**:
- Each oscillator is part of a `SimulationState`
- All oscillators in a simulation are coupled to all others (all-to-all coupling)

**State Transitions**:
- **Initialization**: Created with random phase and frequency
- **Update**: Phase updated each time step based on Kuramoto equation
- **Reset**: Phase and frequency reinitialized with new random values

**Validation Rules**:
- Phase must wrap to [0, 2π) after updates (modulo 2π)
- Intrinsic frequency must be finite (not NaN, not infinity)

---

### 2. SimulationState

Captures the current state of all oscillators and simulation metadata at a given time.

**Fields**:
- `oscillators` (list[Oscillator]): Collection of all oscillators in the simulation
  - Length: N (number of oscillators, user-configurable)
  - Validation: N must be >= 1
  
- `time` (float): Current simulation time
  - Initialization: 0.0
  - Updates: Incremented by Δt (time step) each iteration
  - Validation: Must be >= 0
  
- `resonance_index` (float): Current degree of phase synchronization
  - Range: [0, 1]
  - Calculation: R = |(1/N) Σ e^(iθ_j)| (Kuramoto order parameter)
  - R = 0: Complete desynchronization
  - R = 1: Perfect synchronization
  - Updates: Recalculated each time step after phase updates

**Relationships**:
- Contains multiple `Oscillator` instances
- Used by `VisualizationData` to generate plots

**State Transitions**:
- **Initialization**: Created with N oscillators, time=0, R=0
- **Update**: All oscillator phases updated, time incremented, R recalculated
- **Reset**: Oscillators reinitialized, time reset to 0, R reset to 0

**Validation Rules**:
- Number of oscillators must be >= 1
- Time must be non-negative
- Resonance index must be in [0, 1]

---

### 3. SimulationParameters

User-configurable parameters that control simulation behavior.

**Fields**:
- `num_oscillators` (int): Number of oscillators (N)
  - Range: [1, 1000] (practical limit for performance)
  - Default: 20 (good balance for visualization)
  - Validation: Must be positive integer
  
- `coupling_strength` (float): Strength of coupling between oscillators (K)
  - Range: [0, 10] (practical range, higher values may cause instability)
  - Default: 2.0 (demonstrates clear synchronization)
  - Validation: Must be >= 0, finite
  
- `time_step` (float): Simulation time increment (Δt)
  - Range: (0, 1] (small positive values)
  - Default: 0.01 (good balance of accuracy and speed)
  - Validation: Must be > 0, finite
  
- `frequency_range` (tuple[float, float]): Range for intrinsic frequency distribution
  - Default: (-1.0, 1.0) (symmetric around zero)
  - Validation: First value < second value, both finite
  
- `animation_speed` (float): Visual update rate multiplier
  - Range: [0.1, 10.0] (controls how fast visualizations update)
  - Default: 1.0 (real-time)
  - Validation: Must be > 0, finite

**Relationships**:
- Used by `SimulationState` to initialize and update oscillators
- Modified by user through UI controls

**State Transitions**:
- **Initialization**: Set to default values
- **User Update**: Changed via Streamlit controls (sliders, inputs)
- **Reset**: Parameters remain unchanged (only simulation state resets)

**Validation Rules**:
- All numeric values must be finite (not NaN, not infinity)
- Ranges must be valid (min < max where applicable)
- Positive values must be > 0

---

### 4. VisualizationData

Processed data required to render visualizations.

**Fields**:
- `unit_circle_data` (dict): Data for unit circle plot
  - `x_coords` (list[float]): X coordinates (cos(phase) for each oscillator)
  - `y_coords` (list[float]): Y coordinates (sin(phase) for each oscillator)
  - `phases` (list[float]): Raw phase values for tooltips/labels
  - Updates: Recalculated each time step from oscillator phases
  
- `resonance_history` (list[tuple[float, float]]): Time series of resonance index
  - Format: [(time_0, R_0), (time_1, R_1), ...]
  - Updates: New (time, R) pair appended each time step
  - Bounds: May be limited to last N points for performance (e.g., last 1000 points)
  - Reset: Cleared when simulation resets

**Relationships**:
- Derived from `SimulationState`
- Used by visualization components to render plots

**State Transitions**:
- **Initialization**: Empty or with initial state
- **Update**: New data points added each time step
- **Reset**: History cleared, reinitialized with current state

**Validation Rules**:
- Coordinates must be in [-1, 1] range (unit circle)
- Time values in history must be non-decreasing
- Resonance values must be in [0, 1]

---

### 5. SimulationControlState

State of simulation execution controls.

**Fields**:
- `is_running` (bool): Whether simulation is currently executing
  - Initialization: True (auto-start)
  - Transitions: Toggled by pause/resume button
  
- `is_paused` (bool): Whether simulation is paused
  - Initialization: False
  - Transitions: True when paused, False when resumed/reset

**Relationships**:
- Controls whether `SimulationState` updates occur
- Modified by user through UI buttons

**State Transitions**:
- **Initialization**: is_running=True, is_paused=False
- **Pause**: is_running=False, is_paused=True
- **Resume**: is_running=True, is_paused=False
- **Reset**: is_running=True (if was running), is_paused=False

**Validation Rules**:
- is_running and is_paused cannot both be True simultaneously
- If is_paused=True, then is_running=False

---

## Relationships Summary

```
SimulationParameters
    │
    ├──> SimulationState (uses parameters for initialization and updates)
    │       │
    │       ├──> Oscillator[] (contains N oscillators)
    │       │
    │       └──> VisualizationData (derived from state)
    │
    └──> SimulationControlState (independent, controls execution)
```

## Data Flow

1. **Initialization**:
   - User sets `SimulationParameters` (or uses defaults)
   - `SimulationState` created with N oscillators (random phases/frequencies)
   - `VisualizationData` initialized from initial state
   - `SimulationControlState` set to running

2. **Update Loop** (when running and not paused):
   - `SimulationState` updates all oscillator phases using Kuramoto equation
   - `SimulationState` recalculates resonance index
   - `VisualizationData` updated with new coordinates and resonance value
   - UI renders updated visualizations

3. **Parameter Change**:
   - User modifies `SimulationParameters`
   - If running: Changes take effect immediately on next update
   - If paused: Changes stored, take effect on resume
   - `SimulationState` may need reinitialization (e.g., if N changes)

4. **Reset**:
   - `SimulationState` reinitialized with current parameters
   - `VisualizationData` history cleared
   - `SimulationControlState` reset to running

## Validation Summary

- **Oscillator**: Phase in [0, 2π), frequency finite
- **SimulationState**: N >= 1, time >= 0, R in [0, 1]
- **SimulationParameters**: All values finite, positive where required, valid ranges
- **VisualizationData**: Coordinates in [-1, 1], R in [0, 1], time non-decreasing
- **SimulationControlState**: is_running and is_paused mutually exclusive

