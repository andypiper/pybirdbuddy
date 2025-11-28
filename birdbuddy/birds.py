"""Data models relating to bird Species.

This module provides the Species class for representing bird species data
from the Bird Buddy API, including common names, scientific names, and
favorite foods.
"""

from __future__ import annotations
from collections import UserDict


class Species(UserDict[str, str]):
    """Represents a bird species with identification and dietary information.

    The Species class wraps bird species data from the Bird Buddy API,
    providing access to common names, scientific (Latin) names, and
    favorite foods for the species.

    The class inherits from UserDict, so all dictionary operations are supported.
    Use the provided properties for typed access to common fields.

    Examples:
        >>> species = Species({"id": "NOCA", "name": "Northern Cardinal"})
        >>> species.id
        'NOCA'
        >>> species.name
        'Northern Cardinal'
        >>> species.scientific_name
        'Cardinalis cardinalis'
        >>> species.favorite_foods
        ['SUNFLOWER_SEEDS', 'SAFFLOWER', 'BERRIES']

    Attributes:
        All Species data is stored in the underlying dictionary.
        Use properties for typed access to standard fields.
    """

    @property
    def id(self) -> str:
        """Species id or code"""
        return self["id"]

    @property
    def name(self) -> str:
        """Species common name"""
        return self["name"]

    @property
    def scientific_name(self) -> str | None:
        """Species scientific (Latin) name, or None if not available."""
        return self.get("scientificName")

    @property
    def favorite_foods(self) -> list[str] | None:
        """List of favorite foods (SpeciesBird only), or None if not available."""
        foods = self.get("favoriteFoods")
        return list(foods) if foods is not None else None
