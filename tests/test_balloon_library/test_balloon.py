import pytest
from hab_toolbox.balloon_library import balloon


def test_get_gas_properties():
    known_species, units = balloon.get_gas_properties()
    assert units == 'kg/mol'
    assert known_species['he'] == known_species['helium']


def test_is_valid_balloon():
    assert balloon.is_valid_balloon('HAB-3000') is True
    assert balloon.is_valid_balloon('HAB-9001') is False


def test_radius_from_volume():
    assert balloon._radius_from_volume(1) == 0.6203504908994001
    assert balloon._radius_from_volume(0) == 0
    with pytest.raises(ValueError):
        balloon._radius_from_volume(-1)
