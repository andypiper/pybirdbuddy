"""Bird Buddy media collections and individual media items.

This module provides classes for working with media (images and videos) from
bird sightings, including quality detection, dimensions, processing state,
and media collections organized by species.
"""

from __future__ import annotations
from collections import UserDict
from datetime import datetime
import time
from urllib.parse import urlparse, parse_qs

from .birds import Species
from .feed import FeedNode


class Media(UserDict):
    """Represents a single image or video from a bird sighting.

    The Media class provides access to media metadata including dimensions,
    quality settings, processing state, and content URLs. It distinguishes
    between video and image media types and provides helper methods for
    common operations like slow-motion detection and aspect ratio calculation.

    The class inherits from UserDict, so all dictionary operations are supported.
    Use the provided properties for typed access to media information.

    Examples:
        >>> media = collection.cover_media
        >>> if media.is_video:
        ...     print(f"Video quality: {media.quality}")
        ...     if media.is_slow_motion:
        ...         print("This is a slow-motion video!")
        'Video quality: SLOW_MOTION'
        'This is a slow-motion video!'

        >>> print(f"Dimensions: {media.width}x{media.height}")
        'Dimensions: 1920x1080'

        >>> if media.is_ready:
        ...     url = media.content_url
        ...     print(f"Media ready at: {url}")

    Video Quality Values:
        - K_2: Standard 2K resolution video
        - K_2_ULTRA: Ultra quality 2K video
        - SLOW_MOTION: Slow-motion video capture

    Media State Values:
        - READY: Processing complete, media ready for viewing
        - UPLOADING_STARTED: Upload in progress
        - PROCESSING: Video processing in progress

    Attributes:
        All media data is stored in the underlying dictionary.
        Use properties for typed access to standard fields.
    """

    @property
    def id(self) -> str:
        """The media id"""
        return self["id"]

    @property
    def is_video(self) -> bool:
        """`True` if this Media is a Video item, `False` if Image."""
        return self["__typename"] == "MediaVideo"

    @property
    def created_at(self) -> datetime:
        """Creation timestamp"""
        return FeedNode.parse_datetime(self["createdAt"])

    @property
    def thumbnail_url(self) -> str:
        """Thumbnail URL"""
        return self["thumbnailUrl"]

    @property
    def content_url(self) -> str:
        """Large content URL"""
        return self.get("contentUrl", None)

    @property
    def quality(self) -> str | None:
        """Video quality (K_2, K_2_ULTRA, SLOW_MOTION), or None if not a video or not available."""
        if not self.is_video:
            return None
        return self.get("quality")

    @property
    def state(self) -> str | None:
        """Media processing state (READY, UPLOADING_STARTED, etc.), or None if not available."""
        return self.get("state")

    @property
    def width(self) -> int | None:
        """Media width in pixels, or None if not available."""
        width = self.get("width")
        return int(width) if width is not None else None

    @property
    def height(self) -> int | None:
        """Media height in pixels, or None if not available."""
        height = self.get("height")
        return int(height) if height is not None else None

    @property
    def is_slow_motion(self) -> bool:
        """`True` if this is a slow-motion video, `False` otherwise."""
        return self.quality == "SLOW_MOTION"

    @property
    def aspect_ratio(self) -> float | None:
        """Media aspect ratio (width/height), or None if dimensions not available."""
        if self.width is not None and self.height is not None and self.height > 0:
            return self.width / self.height
        return None

    @property
    def dimensions(self) -> tuple[int, int] | None:
        """Media dimensions as (width, height) tuple, or None if not available."""
        if self.width is not None and self.height is not None:
            return (self.width, self.height)
        return None

    @property
    def is_ready(self) -> bool:
        """`True` if media processing is complete and ready for viewing."""
        return self.state == "READY"

    @property
    def is_expired(self) -> bool:
        """`True` if the media URL is expired"""
        return is_media_expired(self.thumbnail_url)


def is_media_expired(media_url: str) -> bool:
    """`True` if the media URL is expired"""
    if not media_url:
        return None
    expiry = int(parse_qs(urlparse(media_url).query).get("Expires", None).pop())
    if not expiry:
        return None
    now = time.time()
    return expiry < now


class Collection(UserDict):
    """A collection of media organized by bird species.

    Collections group all sightings and media for a particular bird species,
    providing access to visit statistics, cover media, and the species information.

    Examples:
        >>> collections = await bb.refresh_collections()
        >>> for coll in collections.values():
        ...     print(f"{coll.bird_name}: {coll.total_visits} visits")
        ...     print(f"Last seen: {coll.last_visit}")
        'Northern Cardinal: 42 visits'
        'Last seen: 2024-01-15 14:30:00+00:00'

        >>> cover = coll.cover_media
        >>> print(f"Cover media from {coll.feeder_name}")
        'Cover media from Backyard Buddy'

    Attributes:
        All collection data is stored in the underlying dictionary.
        Use properties for typed access to standard fields.
    """

    @property
    def bird_name(self) -> str:
        """The bird species in this collection"""
        return self.get("species", {}).get("name", None)

    @property
    def species(self) -> Species | None:
        """The bird species of this collection"""
        if s := self.get("species", None):
            return Species(s)
        return None

    @property
    def collection_id(self) -> str:
        """The collection ``UUID``"""
        return self["id"]

    @property
    def total_visits(self) -> int:
        """Total number of visits"""
        return int(self.get("visitsAllTime", 0))

    @property
    def last_visit(self) -> datetime:
        """Most recent visit time"""
        return FeedNode.parse_datetime(self["visitLastTime"])

    @property
    def feeder_name(self) -> str | None:
        """The feeder that captured this cover"""
        return self["coverCollectionMedia"].get("feederName")

    @property
    def cover_media(self) -> Media:
        """The cover media"""
        return Media(self["coverCollectionMedia"]["media"])
