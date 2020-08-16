import pytest
import numpy as np
from hab_toolbox.balloon_library import balloon


def test_get_gas_properties():
    known_species, units = balloon.get_gas_properties()
    assert units == 'kg/mol'
    assert 'air' in known_species
    assert known_species['he'] == known_species['helium']


def test_list_known_species():
    assert type(balloon.list_known_species()) == list
    assert len(balloon.list_known_species()) == len(balloon.get_gas_properties()[0])


def test_is_valid_balloon_true():
    assert balloon.is_valid_balloon('HAB-3000') is True


def test_is_valid_balloon_false():
    assert balloon.is_valid_balloon('HAB-3000'.lower()) is False
    assert balloon.is_valid_balloon(10) is False


def test_radius_from_volume():
    assert balloon._radius_from_volume(1) == 0.6203504908994001
    assert balloon._radius_from_volume(0) == 0
    with pytest.raises(ValueError):
        balloon._radius_from_volume(-1)


def test_get_balloon():
    with pytest.raises(ValueError):
        balloon.get_balloon('')
    assert type(balloon.get_balloon('HAB-3000'))
    assert balloon.get_balloon('HAB-3000')['name'] == 'HAB-3000'


def test_gas_initialization():
    with pytest.raises(TypeError):
        # pylint: disable=no-value-for-parameter
        balloon.Gas()
    g = balloon.Gas('air')
    assert g.species == 'air'
    assert g.temperature == balloon.STANDARD_TEMPERATURE_K
    assert g.pressure == balloon.STANDARD_PRESSURE_Pa
    assert g.mass == 0
    assert g.molar_mass == 0.02897


def test_gas_massless():
    g = balloon.Gas('air', mass=0)
    assert g.volume == 0
    assert g.density == 2.5768572246621555


def test_gas_mass():
    g = balloon.Gas('air', mass=1)
    assert g.volume == 0.38806961845979154
    assert g.density == 2.5768572246621555


@pytest.mark.skip(reason="TODO: mock ambiance.Atmosphere object")
def test_gas_match_ambient():
    atmosphere = 'conditions at 100m altitude'
    g = balloon.Gas('air', mass=0)
    g.match_ambient(atmosphere)
    assert g.temperature == np.array([287.50001023])
    assert g.pressure == np.array([100129.45645595])


def test_gas_match_conditions():
    g = balloon.Gas('air', mass=0)
    g.match_conditions(1, 100)
    assert g.temperature == 1
    assert g.pressure == 100


def test_balloon_initialization():
    b = balloon.Balloon('HAB-3000')
    assert b.name == 'HAB-3000'
    assert type(b.lift_gas) == type(balloon.Gas('air'))
    assert b.mass == 3.0


def test_balloon_with_gas():
    g = balloon.Gas('air', mass=1)
    b = balloon.Balloon('HAB-3000', lift_gas=g)
    assert b.volume == g.volume


def test_balloon_burst_threshold():
    g = balloon.Gas('air', mass=1)
    b = balloon.Balloon('HAB-3000', lift_gas=g)
    # override volume
    b.match_conditions(100, .001)
    assert b.burst_threshold_exceeded == True
    b.match_conditions(.001, 1000)
    assert b.burst_threshold_exceeded == False


def test_payload_initialization():
    p = balloon.Payload()
    assert p.dry_mass == 2
    assert p.ballast_mass == 0

    p = balloon.Payload(dry_mass=0, ballast_mass=2)
    assert p.dry_mass == 0
    assert p.ballast_mass == 2


def test_payload_methods():
    p = balloon.Payload()
    assert p.total_mass == 2
