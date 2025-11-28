"""Tests for FeedNode class properties (postcard fields)."""

import pytest
from datetime import datetime
from birdbuddy.feed import FeedNode


class TestFeedNodePostcardFields:
    """Tests for FeedNode postcard-specific properties."""

    def test_postcard_expires_at(self):
        """Test expiresAt field on postcards."""
        node = FeedNode({
            "id": "postcard-123",
            "__typename": "FeedItemNewPostcard",
            "createdAt": "2024-01-01T00:00:00.000+0000",
            "expiresAt": "2024-01-08T00:00:00.000+0000"
        })
        assert node.expires_at is not None
        assert isinstance(node.expires_at, datetime)

    def test_postcard_expires_at_missing(self):
        """Test expiresAt returns None when missing."""
        node = FeedNode({
            "id": "postcard-123",
            "__typename": "FeedItemNewPostcard",
            "createdAt": "2024-01-01T00:00:00.000+0000"
        })
        assert node.expires_at is None

    def test_postcard_has_video_media(self):
        """Test hasVideoMedia field."""
        node = FeedNode({
            "id": "postcard-123",
            "__typename": "FeedItemNewPostcard",
            "hasVideoMedia": True
        })
        assert node.has_video_media is True

    def test_postcard_no_video_media(self):
        """Test hasVideoMedia false."""
        node = FeedNode({
            "id": "postcard-123",
            "__typename": "FeedItemNewPostcard",
            "hasVideoMedia": False
        })
        assert node.has_video_media is False

    def test_postcard_has_video_media_missing(self):
        """Test hasVideoMedia returns None when missing."""
        node = FeedNode({
            "id": "postcard-123",
            "__typename": "FeedItemNewPostcard"
        })
        assert node.has_video_media is None

    def test_postcard_media_image_count(self):
        """Test mediaImageCount field."""
        node = FeedNode({
            "id": "postcard-123",
            "__typename": "FeedItemNewPostcard",
            "mediaImageCount": 3
        })
        assert node.media_image_count == 3

    def test_postcard_media_image_count_zero(self):
        """Test mediaImageCount with zero images."""
        node = FeedNode({
            "id": "postcard-123",
            "__typename": "FeedItemNewPostcard",
            "mediaImageCount": 0
        })
        assert node.media_image_count == 0

    def test_postcard_media_image_count_missing(self):
        """Test mediaImageCount returns None when missing."""
        node = FeedNode({
            "id": "postcard-123",
            "__typename": "FeedItemNewPostcard"
        })
        assert node.media_image_count is None

    def test_postcard_all_new_fields(self):
        """Test postcard with all new fields."""
        node = FeedNode({
            "id": "postcard-complete",
            "__typename": "FeedItemNewPostcard",
            "createdAt": "2024-01-01T12:00:00.000+0000",
            "expiresAt": "2024-01-08T12:00:00.000+0000",
            "hasVideoMedia": True,
            "mediaImageCount": 2
        })
        assert node.node_id == "postcard-complete"
        assert node.created_at is not None
        assert node.expires_at is not None
        assert node.has_video_media is True
        assert node.media_image_count == 2


class TestBackwardCompatibility:
    """Tests for backward compatibility."""

    def test_existing_properties_still_work(self):
        """Test that existing FeedNode properties still work."""
        node = FeedNode({
            "id": "test-node",
            "__typename": "FeedItemNewPostcard",
            "createdAt": "2024-01-01T00:00:00.000+0000"
        })
        # Existing properties
        assert node.node_id == "test-node"
        assert node.node_type.value == "FeedItemNewPostcard"
        assert node.created_at is not None

        # New properties should return None when fields missing
        assert node.expires_at is None
        assert node.has_video_media is None
        assert node.media_image_count is None
