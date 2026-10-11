"""Static checks for Phase 2; these do not call live external APIs."""
import ast
from pathlib import Path

SOURCE = Path(__file__).with_name("bittu.py").read_text(encoding="utf-8")

def test_python_syntax():
    ast.parse(SOURCE)

def test_home_and_panchang_secrets_are_supported():
    for key in ("HOME_LATITUDE", "HOME_LONGITUDE", "PANCHANG_LATITUDE", "PANCHANG_LONGITUDE", "PANCHANG_LOCATION_NAME"):
        assert key in SOURCE

def test_api_payload_uses_resolved_coordinates():
    assert '"latitude": latitude, "longitude": longitude' in SOURCE

def test_astronomy_url_uses_resolved_coordinates():
    assert '"&lng=" + str(longitude)' in SOURCE

def test_coordinate_ranges_are_validated():
    assert "-90 <= lat <= 90" in SOURCE
    assert "-180 <= lon <= 180" in SOURCE

def test_successful_panchang_uses_selected_location_label():
    assert 'fields["location"] = location_name' in SOURCE
    assert 'fields["latitude"] = latitude' in SOURCE
    assert 'fields["longitude"] = longitude' in SOURCE

def test_map_uses_selected_coordinates():
    assert 'HOME_LATITUDE' in SOURCE and 'HOME_LONGITUDE' in SOURCE
    assert 'https://www.google.com/maps?q={home_lat:.6f},{home_lon:.6f}' in SOURCE
