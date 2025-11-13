# Attunement-through-Iterative-Oscillatory-Networks Constitution
<!-- SUGGESTED TEMPLATE - Review and customize before use -->

## Core Principles

### I. Test-Driven Development (NON-NEGOTIABLE)
**MUST**: All core logic (models, simulation, calculations) must have unit tests written before or alongside implementation. Tests must validate mathematical correctness (Kuramoto equations, resonance index calculation) and edge cases (K=0, N=1, etc.).

**SHOULD**: Integration tests for end-to-end simulation flows and UI interactions.

### II. Code Quality & Maintainability
**MUST**: Code must be well-documented with docstrings following module interface contracts. Clear separation of concerns: models (domain logic), visualization (rendering), UI (Streamlit controls).

**SHOULD**: Follow Python PEP 8 style guidelines. Use type hints for function signatures.

### III. Performance Standards
**MUST**: Simulation updates must complete in < 100ms for N=100 oscillators (per contracts/module-interfaces.md). Visualizations must update at 10+ frames per second for up to 100 oscillators (per SC-003).

**SHOULD**: Optimize using NumPy vectorization for O(N²) coupling calculations. Limit resonance_history size for large N to prevent memory issues.

### IV. Error Handling & Edge Cases
**MUST**: All modules must raise appropriate exceptions (ValueError for invalid inputs, TypeError for incorrect types) per contracts/module-interfaces.md. Handle edge cases gracefully: N=1, K=0, very high K, Δt=0/negative, rapid parameter changes, long simulation runs.

**SHOULD**: Provide clear error messages to users for invalid parameter inputs.

### V. Documentation & Educational Value
**MUST**: Educational explanations must be concise and accessible to learners without deep technical background. All key terms (oscillator, phase, resonance, attunement) must be explained.

**SHOULD**: Code comments should explain mathematical concepts where helpful (e.g., Kuramoto equation, order parameter).

## Additional Constraints

### Technology Stack
- **Language**: Python 3.11+ (Streamlit requires 3.8+, 3.11+ recommended)
- **Primary Dependencies**: Streamlit (web framework), Plotly (visualization), NumPy (numerical computations)
- **Testing**: pytest for unit tests, Streamlit testing utilities for integration tests

### Performance Requirements
- Real-time visualization updates: 10+ fps for up to 100 oscillators
- Parameter change response: < 1 second (per SC-002)
- Simulation update: < 100ms for N=100 oscillators

## Development Workflow

### Quality Gates
1. **Before Implementation**: Specification analysis complete, tasks.md generated, constitution compliance verified
2. **During Implementation**: Unit tests pass, integration tests pass, performance benchmarks met
3. **Before Completion**: All acceptance scenarios from spec.md verified, edge cases handled, documentation complete

### Code Review Requirements
- Verify compliance with module interface contracts
- Ensure edge cases are handled
- Validate performance requirements are met
- Check educational content accuracy

## Governance

**Constitution Authority**: This constitution supersedes all other development practices. Any deviation must be explicitly justified and documented.

**Amendments**: Constitution changes require:
- Documentation of rationale
- Impact assessment on existing code
- Approval process (to be defined by project maintainers)

**Compliance Verification**: All `/speckit.analyze` runs must verify constitution compliance. Violations are automatically CRITICAL and require resolution before proceeding.

**Version**: 1.0.0 | **Ratified**: 2025-01-27 | **Last Amended**: 2025-01-27

