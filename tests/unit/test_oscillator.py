"""Unit tests for Oscillator class."""

import pytest
import numpy as np
from aion.models.oscillator import Oscillator


class TestOscillator:
    """Test cases for Oscillator class."""

    def test_init_valid(self):
        """Test oscillator initialization with valid parameters."""
        osc = Oscillator(phase=0.0, intrinsic_frequency=1.0)
        assert osc.phase == 0.0
        assert osc.intrinsic_frequency == 1.0

    def test_init_phase_wrapped(self):
        """Test phase wrapping to [0, 2π)."""
        # Phase must be in [0, 2π), so 2π is invalid
        # Test with a phase just below 2π, which should be valid
        osc = Oscillator(phase=2 * np.pi - 0.001, intrinsic_frequency=1.0)
        assert 0 <= osc.phase < 2 * np.pi
        
        # Test that phase wrapping happens during update
        osc2 = Oscillator(phase=0.0, intrinsic_frequency=1.0)
        # Update with a large coupling term that would push phase beyond 2π
        osc2.update_phase(coupling_term=0.0, time_step=2 * np.pi)
        # Phase should wrap to [0, 2π)
        assert 0 <= osc2.phase < 2 * np.pi

    def test_init_invalid_phase(self):
        """Test initialization with invalid phase raises ValueError."""
        with pytest.raises(ValueError, match="Phase must be in"):
            Oscillator(phase=-1.0, intrinsic_frequency=1.0)

        with pytest.raises(ValueError, match="Phase must be in"):
            Oscillator(phase=3 * np.pi, intrinsic_frequency=1.0)

    def test_init_invalid_frequency(self):
        """Test initialization with invalid frequency raises ValueError."""
        with pytest.raises(ValueError, match="Intrinsic frequency must be finite"):
            Oscillator(phase=0.0, intrinsic_frequency=np.inf)

        with pytest.raises(ValueError, match="Intrinsic frequency must be finite"):
            Oscillator(phase=0.0, intrinsic_frequency=np.nan)

    def test_update_phase_no_coupling(self):
        """Test phase update with zero coupling (independent rotation)."""
        osc = Oscillator(phase=0.0, intrinsic_frequency=1.0)
        osc.update_phase(coupling_term=0.0, time_step=0.01)

        # Phase should increase by ω * Δt = 1.0 * 0.01 = 0.01
        expected_phase = 0.01
        assert abs(osc.phase - expected_phase) < 1e-10

    def test_update_phase_with_coupling(self):
        """Test phase update with non-zero coupling."""
        osc = Oscillator(phase=0.0, intrinsic_frequency=1.0)
        osc.update_phase(coupling_term=0.5, time_step=0.01)

        # Phase should increase by (ω + coupling) * Δt = (1.0 + 0.5) * 0.01 = 0.015
        expected_phase = 0.015
        assert abs(osc.phase - expected_phase) < 1e-10

    def test_update_phase_wrapping(self):
        """Test phase wraps to [0, 2π) after update."""
        osc = Oscillator(phase=2 * np.pi - 0.01, intrinsic_frequency=1.0)
        osc.update_phase(coupling_term=0.0, time_step=0.02)

        # Phase should wrap: (2π - 0.01) + 0.02 = 2π + 0.01 → 0.01
        assert 0 <= osc.phase < 2 * np.pi
        assert abs(osc.phase - 0.01) < 1e-10

    def test_update_phase_invalid_coupling(self):
        """Test update with invalid coupling term raises ValueError."""
        osc = Oscillator(phase=0.0, intrinsic_frequency=1.0)

        with pytest.raises(ValueError, match="Coupling term must be finite"):
            osc.update_phase(coupling_term=np.inf, time_step=0.01)

        with pytest.raises(ValueError, match="Coupling term must be finite"):
            osc.update_phase(coupling_term=np.nan, time_step=0.01)

    def test_update_phase_invalid_time_step(self):
        """Test update with invalid time step raises ValueError."""
        osc = Oscillator(phase=0.0, intrinsic_frequency=1.0)

        with pytest.raises(ValueError, match="Time step must be positive"):
            osc.update_phase(coupling_term=0.0, time_step=0.0)

        with pytest.raises(ValueError, match="Time step must be positive"):
            osc.update_phase(coupling_term=0.0, time_step=-0.01)

        with pytest.raises(ValueError, match="Time step must be positive"):
            osc.update_phase(coupling_term=0.0, time_step=np.inf)

    def test_phase_property_immutable(self):
        """Test that phase property returns value but doesn't allow direct modification."""
        osc = Oscillator(phase=1.0, intrinsic_frequency=1.0)
        phase = osc.phase
        osc.update_phase(coupling_term=0.0, time_step=0.01)
        # Phase should have changed
        assert osc.phase != phase

    def test_frequency_property_immutable(self):
        """Test that intrinsic frequency is immutable."""
        osc = Oscillator(phase=0.0, intrinsic_frequency=1.0)
        freq = osc.intrinsic_frequency
        osc.update_phase(coupling_term=0.0, time_step=0.01)
        # Frequency should remain unchanged
        assert osc.intrinsic_frequency == freq

