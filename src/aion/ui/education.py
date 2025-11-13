"""Educational content for AION simulation."""

import streamlit as st


def render_educational_content() -> None:
    """
    Display educational explanations in Streamlit.

    Contract:
        - Shows definitions for: oscillator, phase, resonance, attunement
        - Explains connections to synchronization, energy minimization, neuro-symbolic binding
        - Uses st.expander() or st.sidebar() for collapsible content
        - Content is concise and accessible
    """
    st.sidebar.header("📚 Educational Content")

    with st.sidebar.expander("🔵 Oscillator", expanded=False):
        st.markdown("""
        An **oscillator** is a node in the AION network that rotates around a unit circle.
        Each oscillator has:
        - **Phase (θ)**: Its current angular position on the circle [0, 2π)
        - **Intrinsic Frequency (ω)**: Its natural rotation rate
        
        In the visualization, each blue dot represents one oscillator. 
        
        **What to Observe:**
        - Initially, oscillators are spread randomly around the circle
        - With sufficient coupling strength (K > 0), they gradually **converge and cluster together**
        - As they synchronize, all oscillators move to approximately the same phase
        - The cluster rotates around the circle as a synchronized group
        """)

    with st.sidebar.expander("🔄 Phase", expanded=False):
        st.markdown("""
        **Phase** is the angular position of an oscillator on the unit circle, measured
        in radians from 0 to 2π.
        
        - **Phase = 0**: Oscillator at position (1, 0) on the circle
        - **Phase = π/2**: Oscillator at position (0, 1)
        - **Phase = π**: Oscillator at position (-1, 0)
        - **Phase = 3π/2**: Oscillator at position (0, -1)
        
        The unit circle visualization shows each oscillator's phase as a point at
        coordinates (cos(θ), sin(θ)). As oscillators synchronize, their phases
        converge, causing them to cluster together on the circle.
        """)

    with st.sidebar.expander("📈 Resonance", expanded=False):
        st.markdown("""
        **Resonance** is the degree of phase synchronization among oscillators,
        measured by the resonance index R ∈ [0, 1].
        
        - **R = 0**: Complete desynchronization (oscillators spread evenly around circle)
        - **R = 1**: Perfect synchronization (all oscillators clustered at same phase)
        
        The resonance index is calculated as:
        ```
        R = |(1/N) Σ e^(iθ_j)|
        ```
        where N is the number of oscillators and θ_j is the phase of oscillator j.
        
        **What to Observe:**
        - Initially, R is low (typically 0.1-0.3) when oscillators are spread out
        - As oscillators **converge and cluster together**, R increases toward 1.0
        - Watch the resonance chart: the line should trend upward over time
        - Higher coupling strength (K) leads to faster convergence and higher R values
        - With K=0, oscillators rotate independently and R remains low
        """)

    with st.sidebar.expander("🎯 Attunement", expanded=False):
        st.markdown("""
        **Attunement** is the process by which oscillators align their phases through
        coupling, creating coherent collective behavior.
        
        In the AION model, attunement emerges from the Kuramoto equation:
        ```
        dθ_j/dt = ω_j + (K/N) Σ sin(θ_k - θ_j)
        ```
        
        Each oscillator adjusts its phase based on:
        - Its own intrinsic frequency (ω_j)
        - The average influence of all other oscillators (coupling term)
        
        **Phase Coupling and Meaning:**
        Phase coupling represents how **meaning emerges through interactions**—oscillators
        "communicate" through their phase relationships, leading to synchronized behavior.
        Just as neurons in the brain communicate through synchronized firing patterns, oscillators
        in the AION network communicate through phase alignment, creating coherent representations
        that emerge from their collective interactions.
        
        **What to Observe:**
        - With **low coupling (K ≈ 0)**: Oscillators rotate independently, staying spread out
        - With **moderate coupling (K ≈ 2-3)**: Oscillators gradually **converge and cluster** together over time
        - With **high coupling (K > 5)**: Oscillators quickly synchronize into a tight cluster
        - The clustered oscillators rotate together around the circle as a synchronized group
        - This clustering represents the **emergence of coherent meaning through phase alignment**
        """)

    with st.sidebar.expander("🌐 Broader Connections", expanded=False):
        st.markdown("""
        The AION model connects to several important concepts:
        
        **Phase Coupling and Communication**: In the AION model, **phase coupling represents
        how meaning emerges through interactions**—oscillators "communicate" through their phase
        relationships, leading to synchronized behavior. This mirrors how neurons in the brain
        communicate through synchronized firing patterns to create coherent perceptions.
        
        **Synchronization**: Oscillators naturally synchronize when coupled, similar to
        fireflies flashing in unison or neurons firing together in the brain. This synchronization
        emerges from the communication between oscillators through phase coupling.
        
        **Energy Minimization**: Synchronized states represent lower energy configurations,
        as the system minimizes phase differences through coupling. The communication between
        oscillators drives the system toward these stable, low-energy states.
        
        **Neuro-Symbolic Binding**: In cognitive science, oscillatory networks can bind
        different features (e.g., color and shape) into unified percepts through phase
        synchronization. The phase coupling mechanism enables this binding by allowing
        oscillators representing different features to communicate and align.
        
        **Quantum-Inspired Computing**: The AION architecture draws inspiration from
        quantum mechanics, where phase relationships encode information and meaning
        emerges through interference patterns. Phase coupling enables this information
        encoding and meaning emergence.
        
        **Phase Coupling vs. Reinforcement Learning**: While both involve feedback and
        convergence to stable states, phase coupling differs from reinforcement learning:
        - **Similarities**: Both use feedback mechanisms and converge to optimal/stable states
        - **Differences**: Phase coupling has implicit "rewards" (energy minimization) rather
          than explicit rewards, is deterministic rather than stochastic, and is collective
          rather than individual. Phase coupling is more like physics-based self-organization
          or collective intelligence, where meaning emerges naturally from interactions.
        
        **AION vs. Diffusion Models**: While both use differential equations and show order
        from disorder, they serve different purposes:
        - **Similarities**: Both involve differential equations, transitions from disorder to
          order, and can include stochastic processes
        - **Differences**: Diffusion models are generative (create new data by reversing noise),
          while AION is about synchronization (aligning phases). Diffusion models learn data
          distributions, while AION follows physics-based dynamics. AION is more like
          reaction-diffusion systems or self-organization, where meaning emerges from
          collective interactions rather than learned denoising.
        """)

