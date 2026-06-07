"""Shared pytest fixtures and configuration for the SkyNet test suite."""

import pytest


@pytest.fixture
def sample_iata_codes():
    """Provide sample valid IATA codes for testing."""
    return ["LHR", "JFK", "DXB", "CDG", "SIN", "HKG", "LAX", "NRT"]


@pytest.fixture
def sample_routes():
    """Provide sample flight routes with distances for testing."""
    return [
        ("LHR", "CDG", 340),
        ("LHR", "JFK", 5500),
        ("CDG", "DXB", 5200),
        ("DXB", "SIN", 5800),
        ("JFK", "LAX", 3900),
        ("SIN", "HKG", 2500),
        ("HKG", "NRT", 2900),
    ]
