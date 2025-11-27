"""Bird Buddy collections and media"""

from __future__ import annotations
from collections import UserDict
from datetime import datetime
import time
from urllib.parse import urlparse, parse_qs

from .birds import Species
from .feed import FeedNode


class Media(UserDict):
    """Represents one ``MediaImage`` or ``MediaVideo`` type"""

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
    """Collection of media for a particular bird species."""

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
