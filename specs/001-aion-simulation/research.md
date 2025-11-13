# Research: AION Educational Simulation

**Date**: 2025-01-27  
**Feature**: 001-aion-simulation  
**Purpose**: Resolve technical clarifications identified in implementation plan

## Research Questions

### 1. Visualization Library Choice: Plotly vs Matplotlib

**Question**: Which visualization library should be used for real-time updates in Streamlit?

**Decision**: **Plotly**

**Rationale**:
- **Native Streamlit Integration**: Streamlit provides `st.plotly_chart()` with built-in support for Plotly figures, enabling seamless real-time updates
- **Interactive Capabilities**: Plotly offers superior interactivity (zoom, pan, hover tooltips) which enhances educational value
- **Performance**: Plotly is optimized for web-based visualizations and handles frequent updates more efficiently than Matplotlib in Streamlit contexts
- **Animation Support**: Plotly has built-in animation capabilities (`plotly.graph_objects.Figure`) that work well with Streamlit's rerun mechanism
- **Real-time Updates**: Plotly figures can be updated efficiently by modifying the figure object and re-rendering, whereas Matplotlib requires more complex handling in Streamlit
- **Unit Circle Visualization**: Plotly's `scatter` plots with polar coordinates or standard 2D plots work excellently for unit circle representations
- **Time Series Charts**: Plotly's `plotly.graph_objects.Scatter` is ideal for the resonance index line chart with smooth updates

**Alternatives Considered**:
- **Matplotlib**: While powerful and widely used, Matplotlib requires `st.pyplot()` which can be slower for real-time updates and lacks the interactive features that enhance educational value. Matplotlib animations in Streamlit require more complex state management.
- **Altair**: Another option, but Plotly has better performance characteristics for frequent updates and more intuitive API for this use case.

**Implementation Notes**:
- Use `plotly.graph_objects` for programmatic figure creation
- Leverage `plotly.express` for simpler chart types if needed
- Store figure objects in Streamlit session state for efficient updates
- Use `st.plotly_chart(fig, use_container_width=True)` for responsive layout

---

### 2. Streamlit Testing Approach

**Question**: How should Streamlit applications be tested, particularly for unit testing simulation logic?

**Decision**: **Hybrid Testing Approach - pytest for core logic + Streamlit testing utilities for UI**

**Rationale**:
- **Separation of Concerns**: The core simulation logic (Kuramoto equations, oscillator models) should be testable independently of Streamlit, enabling fast unit tests
- **pytest Standard**: Use pytest for all unit tests of business logic (oscillator phase updates, resonance index calculations, simulation state management)
- **Streamlit Testing**: For UI components and Streamlit-specific behavior, use Streamlit's testing utilities or mock Streamlit components
- **Testability**: By keeping simulation logic in separate modules (`src/aion/models/`), we can test the mathematical correctness without Streamlit overhead
- **Integration Testing**: Use pytest with Streamlit's test client or mocking for integration tests that verify UI interactions

**Alternatives Considered**:
- **Pure Streamlit Testing**: Testing everything through Streamlit would be slower and harder to maintain. Core logic should be framework-agnostic.
- **No Testing**: Not acceptable for educational software where correctness of mathematical models is critical.

**Implementation Notes**:
- **Unit Tests**: Test `Oscillator`, `Simulation` classes with pytest, verifying:
  - Phase update calculations match Kuramoto equation
  - Resonance index calculation correctness
  - Edge cases (K=0, N=1, etc.)
- **Integration Tests**: Test Streamlit app flow with:
  - Mock Streamlit components or use `streamlit.testing` utilities
  - Verify parameter changes affect simulation correctly
  - Test pause/resume/reset functionality
- **Test Structure**:
  ```
  tests/unit/          # Pure pytest, no Streamlit imports
  tests/integration/   # May import Streamlit, test app.py
  ```
- **Dependencies**: Add `pytest`, `pytest-cov` to requirements.txt. Consider `streamlit.testing` if available for UI testing.

---

## Summary

All technical clarifications have been resolved:

1. ✅ **Visualization Library**: Plotly selected for superior Streamlit integration, performance, and interactivity
2. ✅ **Testing Approach**: Hybrid approach using pytest for core logic and Streamlit testing utilities for UI components

## Updated Technical Context

Based on this research, the implementation plan's Technical Context section should be updated:

- **Primary Dependencies**: Streamlit, Plotly, NumPy (remove "NEEDS CLARIFICATION")
- **Testing**: pytest for unit tests, Streamlit testing utilities for integration tests (remove "NEEDS CLARIFICATION")

## Next Steps

Proceed to Phase 1: Design & Contracts
- Generate `data-model.md` from feature spec entities
- Generate API contracts (if applicable for Streamlit app)
- Generate `quickstart.md`
- Update agent context

