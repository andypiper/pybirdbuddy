"""Bird Buddy API Library for Python.

This library provides a Python interface to the Bird Buddy GraphQL API,
allowing you to access and manage your Bird Buddy smart bird feeder.

Main Components:
    - BirdBuddy: Main client class for API interactions
    - Feeder: Represents a Bird Buddy device with battery, signal, and configuration
    - Media: Video and image media from bird sightings
    - Collection: Organized collections of media by species
    - Feed: Activity feed of postcards and events
    - Species: Bird species information with scientific names and favorite foods
    - Sighting: Bird sighting data and recognition results

Basic Usage:
    >>> from birdbuddy import BirdBuddy
    >>> bb = BirdBuddy(email="user@example.com", password="secret")
    >>> await bb.refresh()
    >>> for feeder in bb.feeders.values():
    ...     print(f"{feeder.name}: {feeder.battery.percentage}%")

Features:
    - Async/await API using GraphQL
    - Complete feeder management (settings, firmware updates, power profiles)
    - Media access with quality detection (including slow-motion videos)
    - Bird species recognition and sighting collection
    - Feed monitoring for new postcards and events
    - Collections management by species
    - Video capabilities detection and configuration
    - Postcard expiration tracking

For complete documentation, see the individual module and class docstrings.
"""

import logging

LOGGER = logging.getLogger(__package__)
VERBOSE = int(logging.DEBUG / 2)
# VERBOSE = 2 * VERBOSE
