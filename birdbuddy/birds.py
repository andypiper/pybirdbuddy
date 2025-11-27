"""Data models relating to bird Species"""

from __future__ import annotations
from collections import UserDict


class Species(UserDict[str, str]):
    """Species"""

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
