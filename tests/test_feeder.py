"""Tests for Feeder class properties."""

import pytest
from birdbuddy.feeder import Feeder


class TestFeederHousingType:
    """Tests for Feeder housing_type property."""

    def test_feeder_with_housing_type(self):
        """Test feeder with housingType field."""
        feeder = Feeder({
            "id": "feeder-123",
            "name": "My Feeder",
            "state": "READY_TO_STREAM",
            "housingType": "STANDARD",
            "__typename": "FeederForOwner"
        })
        assert feeder.housing_type == "STANDARD"

    def test_feeder_without_housing_type(self):
        """Test backward compatibility when housingType is missing."""
        feeder = Feeder({
            "id": "feeder-123",
            "name": "My Feeder",
            "state": "READY_TO_STREAM",
            "__typename": "FeederForOwner"
        })
        assert feeder.housing_type is None

    def test_feeder_housing_types(self):
        """Test various housing type values."""
        housing_types = ["STANDARD", "HUMMINGBIRD", "CUSTOM"]
        for ht in housing_types:
            feeder = Feeder({
                "id": f"feeder-{ht}",
                "name": "Test Feeder",
                "state": "ONLINE",
                "housingType": ht,
                "__typename": "FeederForPrivate"
            })
            assert feeder.housing_type == ht


class TestFeederVersion:
    """Tests for Feeder version properties."""

    def test_feeder_with_firmware_version(self):
        """Test feeder with firmwareVersion (owner-only field)."""
        feeder = Feeder({
            "id": "feeder-123",
            "name": "My Feeder",
            "state": "ONLINE",
            "firmwareVersion": "1.2.3",
            "__typename": "FeederForOwner"
        })
        assert feeder.version == "1.2.3"
        assert feeder.device_version is None

    def test_feeder_with_device_version(self):
        """Test feeder with version field."""
        feeder = Feeder({
            "id": "feeder-123",
            "name": "My Feeder",
            "state": "ONLINE",
            "version": "v2.0.0",
            "__typename": "FeederForPrivate"
        })
        assert feeder.device_version == "v2.0.0"
        assert feeder.version == "v2.0.0"

    def test_feeder_with_both_versions(self):
        """Test feeder with both firmwareVersion and version fields."""
        feeder = Feeder({
            "id": "feeder-123",
            "name": "My Feeder",
            "state": "ONLINE",
            "firmwareVersion": "1.2.3",
            "version": "v2.0.0",
            "__typename": "FeederForOwner"
        })
        # version property should prefer firmwareVersion
        assert feeder.version == "1.2.3"
        assert feeder.device_version == "v2.0.0"

    def test_feeder_without_version(self):
        """Test backward compatibility when version fields are missing."""
        feeder = Feeder({
            "id": "feeder-123",
            "name": "My Feeder",
            "state": "ONLINE",
            "__typename": "FeederForPrivate"
        })
        assert feeder.version is None
        assert feeder.device_version is None

    def test_feeder_version_update_available(self):
        """Test version update availability."""
        feeder = Feeder({
            "id": "feeder-123",
            "name": "My Feeder",
            "state": "ONLINE",
            "firmwareVersion": "1.2.3",
            "availableFirmwareVersion": "1.3.0",
            "__typename": "FeederForOwner"
        })
        assert feeder.version == "1.2.3"
        assert feeder.version_update_available == "1.3.0"


class TestFeederComplete:
    """Tests for feeder with all new fields."""

    def test_feeder_all_new_fields(self):
        """Test feeder with all new Phase 3 fields."""
        feeder = Feeder({
            "id": "feeder-complete",
            "name": "Complete Feeder",
            "state": "READY_TO_STREAM",
            "housingType": "STANDARD",
            "version": "v2.1.0",
            "firmwareVersion": "2.1.0",
            "availableFirmwareVersion": "2.2.0",
            "__typename": "FeederForOwner",
            "battery": {
                "percentage": 85,
                "charging": False,
                "state": "HIGH"
            },
            "signal": {
                "value": -45,
                "state": "HIGH"
            }
        })
        # New fields
        assert feeder.housing_type == "STANDARD"
        assert feeder.device_version == "v2.1.0"
        assert feeder.version == "2.1.0"
        assert feeder.version_update_available == "2.2.0"

        # Existing fields should still work
        assert feeder.id == "feeder-complete"
        assert feeder.name == "Complete Feeder"
        assert feeder.battery.percentage == 85
        assert feeder.signal.rssi == -45


class TestBackwardCompatibility:
    """Tests for backward compatibility."""

    def test_existing_properties_still_work(self):
        """Test that existing feeder properties still work."""
        feeder = Feeder({
            "id": "test-feeder",
            "name": "Test Bird Buddy",
            "state": "ONLINE",
            "serialNumber": "BB-12345",
            "__typename": "FeederForOwner",
            "battery": {
                "percentage": 75,
                "charging": True,
                "state": "MEDIUM"
            }
        })
        # Existing properties
        assert feeder.id == "test-feeder"
        assert feeder.name == "Test Bird Buddy"
        assert feeder.serial == "BB-12345"
        assert feeder.is_owner is True
        assert feeder.battery.percentage == 75
        assert feeder.battery.is_charging is True

        # New properties should return None when fields missing
        assert feeder.housing_type is None
        assert feeder.device_version is None

    def test_dict_access_still_works(self):
        """Test that dict-style access still works (Feeder extends UserDict)."""
        feeder = Feeder({
            "id": "test-feeder",
            "name": "Test Feeder",
            "housingType": "STANDARD",
            "version": "v1.0.0"
        })
        # Dict-style access should work
        assert feeder["id"] == "test-feeder"
        assert feeder["housingType"] == "STANDARD"
        assert feeder["version"] == "v1.0.0"

        # Property access should also work
        assert feeder.housing_type == "STANDARD"
        assert feeder.device_version == "v1.0.0"
