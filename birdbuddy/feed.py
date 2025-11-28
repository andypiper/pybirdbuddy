"""Bird Buddy activity feed and feed items.

This module provides classes for working with the Bird Buddy activity feed,
including postcards, sightings, species unlocks, and other feed events.
Feed items contain information about expiration times, media content, and
timestamps.
"""

from __future__ import annotations

from collections import UserDict
from datetime import datetime
from enum import Enum

from propcache import cached_property

from . import LOGGER


class FeedNodeType(Enum):
    """Types of items that can appear in the Bird Buddy feed.

    Feed items represent different events and activities from your feeders,
    from new bird sightings to feeder sharing events.

    Values:
        NewPostcard: A new postcard with bird sighting(s) ready to collect
        CollectedPostcard: A postcard that has been collected
        SpeciesSighting: A sighting of a bird species
        SpeciesUnlocked: First sighting of a new species (unlocked)
        MysteryVisitorNotRecognized: An unidentified bird visitor
        MysteryVisitorResolved: A mystery visitor that was later identified
        MediaLiked: Someone liked media from your feeder
        InvitationConfirmed: A feeder sharing invitation was accepted
        InvitationDeclined: A feeder sharing invitation was declined
        MemberDeleted: A member was removed from feeder access
        GlobalImportant: Important announcement from Bird Buddy
        GlobalRegular: Regular announcement from Bird Buddy
        Unknown: An unrecognized feed item type
    """

    CollectedPostcard = "FeedItemCollectedPostcard"
    GlobalImportant = "FeedGlobalImportantItem"
    GlobalRegular = "FeedGlobalRegularItem"
    InvitationConfirmed = "FeedItemFeederInvitationConfirmed"
    InvitationDeclined = "FeedItemFeederInvitationDeclined"
    MemberDeleted = "FeedItemFeederMemberDeleted"
    MediaLiked = "FeedItemMediaLiked"
    MysteryVisitorNotRecognized = "FeedItemMysteryVisitorNotRecognized"
    MysteryVisitorResolved = "FeedItemMysteryVisitorResolved"
    NewPostcard = "FeedItemNewPostcard"
    SpeciesSighting = "FeedItemSpeciesSighting"
    SpeciesUnlocked = "FeedItemSpeciesUnlocked"

    Unknown = "Unknown"
    """Sentinel value for an unexpected feed type."""

    @classmethod
    def _missing_(cls, value: str):
        LOGGER.warning("Unexpected Feed type: %s", value)
        return FeedNodeType.Unknown


class FeedNode(UserDict[str, any]):
    """A single item in the Bird Buddy activity feed.

    Feed nodes represent individual events like new postcards, sightings,
    species unlocks, and other activities. Each node has a type, timestamp,
    and type-specific data.

    For NewPostcard nodes, additional properties provide information about
    media content, expiration times, and whether the postcard contains video.

    The class inherits from UserDict, so all dictionary operations are supported.
    Use the provided properties for typed access to feed item data.

    Examples:
        >>> feed = await bb.feed()
        >>> for node in feed.nodes:
        ...     if node.node_type == FeedNodeType.NewPostcard:
        ...         print(f"New postcard expires: {node.expires_at}")
        ...         print(f"Has video: {node.has_video_media}")
        ...         print(f"Image count: {node.media_image_count}")

        >>> new_items = feed.filter(of_type=FeedNodeType.NewPostcard)
        >>> for item in new_items:
        ...     print(f"Created: {item.created_at}")

    Attributes:
        All feed node data is stored in the underlying dictionary.
        Use properties for typed access to standard fields.

    Note:
        Properties like expires_at, has_video_media, and media_image_count
        are specific to NewPostcard feed items and will return None for
        other feed item types.
    """

    _DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%S.%f%z"
    """The format string of GraphQL timestamps. This is not guaranteed to conform to
    :func:`datetime.fromisoformat()`, so it has to be parsed manually."""

    @staticmethod
    def parse_datetime(timestr: str | None) -> datetime | None:
        """Convert a time string into `datetime`."""
        if timestr is None:
            return None
        if len(timestr) == 24:
            # The known expected datetime format in the BirdBuddy feed
            return datetime.strptime(timestr, FeedNode._DATETIME_FORMAT)
        return datetime.fromisoformat(timestr)

    @property
    def node_id(self) -> str:
        """The Feed node id."""
        return self["id"]

    @property
    def node_type(self) -> FeedNodeType:
        """The feed node type."""
        return FeedNodeType(self.get("__typename"))

    @property
    def created_at(self) -> datetime | None:
        """The `datetime` when the FeedNode item was created."""
        return FeedNode.parse_datetime(self.get("createdAt"))

    @property
    def expires_at(self) -> datetime | None:
        """The `datetime` when the postcard expires (FeedItemNewPostcard only), or None."""
        return FeedNode.parse_datetime(self.get("expiresAt"))

    @property
    def has_video_media(self) -> bool | None:
        """True if postcard contains video (FeedItemNewPostcard only), or None if not a postcard."""
        return self.get("hasVideoMedia")

    @property
    def media_image_count(self) -> int | None:
        """Number of images in postcard (FeedItemNewPostcard only), or None if not a postcard."""
        count = self.get("mediaImageCount")
        return int(count) if count is not None else None


class FeedEdge(UserDict[str, any]):
    """A single edge in the feed's paginated structure.

    Feed edges wrap feed nodes and provide cursor information for pagination.
    Most users will interact with feed nodes directly rather than edges.

    Examples:
        >>> feed = await bb.feed()
        >>> for edge in feed.edges:
        ...     print(f"Cursor: {edge.cursor}")
        ...     print(f"Node type: {edge.node.node_type}")
    """

    @property
    def cursor(self) -> str:
        """Feed edge cursor."""
        return self.get("cursor")

    @property
    def node(self) -> FeedNode:
        """Feed edge node."""
        return FeedNode(self.get("node"))


class Feed(UserDict[str, any]):
    """The Bird Buddy activity feed containing all recent events and postcards.

    The Feed class provides access to the paginated activity feed, supporting
    filtering by type and time, and pagination for retrieving older items.

    Examples:
        >>> feed = await bb.feed()
        >>> print(f"Feed has {len(list(feed.nodes))} items")

        >>> # Get only new postcards
        >>> postcards = feed.filter(of_type=FeedNodeType.NewPostcard)
        >>> for postcard in postcards:
        ...     print(f"Postcard expires: {postcard.expires_at}")

        >>> # Get items newer than a specific time
        >>> recent = feed.filter(newer_than=datetime(2024, 1, 1))

        >>> # Pagination - get next page
        >>> if feed.page_end_cursor:
        ...     older_feed = await bb.feed(after=feed.page_end_cursor)

    Attributes:
        All feed data is stored in the underlying dictionary.
        Use properties and methods for typed access to feed items.
    """

    @property
    def edges(self) -> list[FeedEdge]:
        """Returns all edges of the Feed."""
        return (FeedEdge(edge) for edge in self.get("edges", []))

    @property
    def nodes(self) -> list[FeedNode]:
        """Returns all nodes of the Feed edges."""
        return (edge.node for edge in self.edges)

    @property
    def page_end_cursor(self) -> str:
        """The cursor used to access the next (older) page of feed items."""
        return self.get("pageInfo", {}).get("endCursor", None)

    @cached_property
    def newest_edge(self) -> FeedEdge | None:
        """Returns the newest `FeedEdge`, by `FeedNode.created_at`."""
        return max(
            (e for e in self.edges if e.node.created_at),
            key=lambda edge: edge.node.created_at,
            default=None,
        )

    def filter(
        self,
        of_type: FeedNodeType | list[FeedNodeType] = None,
        newer_than: datetime | None = None,
    ) -> list[FeedNode]:
        """Filter the feed by type or time."""
        if isinstance(of_type, FeedNodeType):
            of_type = [of_type]
        return [
            node
            for node in self.nodes
            if (of_type is None or node.node_type in of_type)
            and (
                newer_than is None or (node.created_at and node.created_at > newer_than)
            )
        ]
