"""Tests for Species class properties."""

import pytest
from birdbuddy.birds import Species


class TestSpecies:
    """Tests for Species properties."""

    def test_species_with_scientific_name(self):
        """Test species with scientificName field."""
        species = Species({
            "id": "species-123",
            "name": "American Robin",
            "scientificName": "Turdus migratorius",
            "iconUrl": "https://example.com/robin.jpg",
            "description": "A common North American bird"
        })
        assert species.id == "species-123"
        assert species.name == "American Robin"
        assert species.scientific_name == "Turdus migratorius"

    def test_species_without_scientific_name(self):
        """Test backward compatibility when scientificName is missing."""
        species = Species({
            "id": "species-123",
            "name": "American Robin",
            "iconUrl": "https://example.com/robin.jpg",
            "description": "A common North American bird"
        })
        assert species.id == "species-123"
        assert species.name == "American Robin"
        assert species.scientific_name is None

    def test_species_with_empty_scientific_name(self):
        """Test species with empty scientificName."""
        species = Species({
            "id": "species-123",
            "name": "Mystery Bird",
            "scientificName": "",
            "iconUrl": "https://example.com/mystery.jpg"
        })
        assert species.scientific_name == ""

    def test_species_minimal(self):
        """Test species with only required fields."""
        species = Species({
            "id": "species-456",
            "name": "Unknown Bird"
        })
        assert species.id == "species-456"
        assert species.name == "Unknown Bird"
        assert species.scientific_name is None


class TestBackwardCompatibility:
    """Tests for backward compatibility."""

    def test_existing_code_still_works(self):
        """Test that existing code accessing id and name still works."""
        species = Species({
            "id": "test-id",
            "name": "Test Bird"
        })
        # Existing properties should work
        assert species.id == "test-id"
        assert species.name == "Test Bird"
        # New property should return None when field missing
        assert species.scientific_name is None

    def test_dict_access_still_works(self):
        """Test that dict-style access still works (Species extends UserDict)."""
        species = Species({
            "id": "test-id",
            "name": "Test Bird",
            "scientificName": "Testus birdus"
        })
        # Dict-style access should work
        assert species["id"] == "test-id"
        assert species["name"] == "Test Bird"
        assert species["scientificName"] == "Testus birdus"
        # Property access should also work
        assert species.scientific_name == "Testus birdus"
