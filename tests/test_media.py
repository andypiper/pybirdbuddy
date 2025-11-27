"""Tests for Media class properties and methods."""

import pytest
from birdbuddy.media import Media


class TestMediaVideo:
    """Tests for MediaVideo properties."""

    def test_video_quality_slow_motion(self):
        """Test quality field returns SLOW_MOTION for slow-motion videos."""
        video = Media({
            "__typename": "MediaVideo",
            "id": "test-id",
            "createdAt": "2024-01-01T00:00:00Z",
            "thumbnailUrl": "https://example.com/thumb.jpg",
            "quality": "SLOW_MOTION",
        })
        assert video.quality == "SLOW_MOTION"
        assert video.is_slow_motion is True

    def test_video_quality_k2(self):
        """Test quality field returns K_2 for standard videos."""
        video = Media({
            "__typename": "MediaVideo",
            "id": "test-id",
            "createdAt": "2024-01-01T00:00:00Z",
            "thumbnailUrl": "https://example.com/thumb.jpg",
            "quality": "K_2",
        })
        assert video.quality == "K_2"
        assert video.is_slow_motion is False

    def test_video_quality_missing(self):
        """Test quality returns None when field is missing."""
        video = Media({
            "__typename": "MediaVideo",
            "id": "test-id",
            "createdAt": "2024-01-01T00:00:00Z",
            "thumbnailUrl": "https://example.com/thumb.jpg",
        })
        assert video.quality is None
        assert video.is_slow_motion is False

    def test_video_state_ready(self):
        """Test state field returns READY for processed videos."""
        video = Media({
            "__typename": "MediaVideo",
            "id": "test-id",
            "createdAt": "2024-01-01T00:00:00Z",
            "thumbnailUrl": "https://example.com/thumb.jpg",
            "state": "READY",
        })
        assert video.state == "READY"
        assert video.is_ready is True

    def test_video_state_uploading(self):
        """Test state field returns UPLOADING_STARTED for uploading videos."""
        video = Media({
            "__typename": "MediaVideo",
            "id": "test-id",
            "createdAt": "2024-01-01T00:00:00Z",
            "thumbnailUrl": "https://example.com/thumb.jpg",
            "state": "UPLOADING_STARTED",
        })
        assert video.state == "UPLOADING_STARTED"
        assert video.is_ready is False

    def test_video_dimensions(self):
        """Test width and height fields for videos."""
        video = Media({
            "__typename": "MediaVideo",
            "id": "test-id",
            "createdAt": "2024-01-01T00:00:00Z",
            "thumbnailUrl": "https://example.com/thumb.jpg",
            "width": 960,
            "height": 1280,
        })
        assert video.width == 960
        assert video.height == 1280
        assert video.dimensions == (960, 1280)
        assert video.aspect_ratio == pytest.approx(0.75)

    def test_video_dimensions_missing(self):
        """Test dimensions return None when fields are missing."""
        video = Media({
            "__typename": "MediaVideo",
            "id": "test-id",
            "createdAt": "2024-01-01T00:00:00Z",
            "thumbnailUrl": "https://example.com/thumb.jpg",
        })
        assert video.width is None
        assert video.height is None
        assert video.dimensions is None
        assert video.aspect_ratio is None

    def test_video_all_new_fields(self):
        """Test video with all new fields populated."""
        video = Media({
            "__typename": "MediaVideo",
            "id": "test-id",
            "createdAt": "2024-01-01T00:00:00Z",
            "thumbnailUrl": "https://example.com/thumb.jpg",
            "contentUrl": "https://example.com/video.mp4",
            "quality": "SLOW_MOTION",
            "state": "READY",
            "width": 960,
            "height": 1280,
        })
        assert video.is_video is True
        assert video.quality == "SLOW_MOTION"
        assert video.is_slow_motion is True
        assert video.state == "READY"
        assert video.is_ready is True
        assert video.width == 960
        assert video.height == 1280
        assert video.dimensions == (960, 1280)
        assert video.aspect_ratio == pytest.approx(0.75)


class TestMediaImage:
    """Tests for MediaImage properties."""

    def test_image_quality_none(self):
        """Test quality returns None for images."""
        image = Media({
            "__typename": "MediaImage",
            "id": "test-id",
            "createdAt": "2024-01-01T00:00:00Z",
            "thumbnailUrl": "https://example.com/thumb.jpg",
        })
        assert image.quality is None
        assert image.is_slow_motion is False

    def test_image_state_ready(self):
        """Test state field returns READY for processed images."""
        image = Media({
            "__typename": "MediaImage",
            "id": "test-id",
            "createdAt": "2024-01-01T00:00:00Z",
            "thumbnailUrl": "https://example.com/thumb.jpg",
            "state": "READY",
        })
        assert image.state == "READY"
        assert image.is_ready is True

    def test_image_dimensions(self):
        """Test width and height fields for images."""
        image = Media({
            "__typename": "MediaImage",
            "id": "test-id",
            "createdAt": "2024-01-01T00:00:00Z",
            "thumbnailUrl": "https://example.com/thumb.jpg",
            "width": 1920,
            "height": 1080,
        })
        assert image.width == 1920
        assert image.height == 1080
        assert image.dimensions == (1920, 1080)
        assert image.aspect_ratio == pytest.approx(1.777777, rel=1e-4)

    def test_image_all_new_fields(self):
        """Test image with all new fields populated."""
        image = Media({
            "__typename": "MediaImage",
            "id": "test-id",
            "createdAt": "2024-01-01T00:00:00Z",
            "thumbnailUrl": "https://example.com/thumb.jpg",
            "contentUrl": "https://example.com/image.jpg",
            "state": "READY",
            "width": 1920,
            "height": 1080,
        })
        assert image.is_video is False
        assert image.quality is None  # Images don't have quality
        assert image.is_slow_motion is False
        assert image.state == "READY"
        assert image.is_ready is True
        assert image.width == 1920
        assert image.height == 1080
        assert image.dimensions == (1920, 1080)


class TestBackwardCompatibility:
    """Tests for backward compatibility with existing code."""

    def test_existing_properties_still_work(self):
        """Test that existing properties still work as expected."""
        media = Media({
            "__typename": "MediaVideo",
            "id": "test-id",
            "createdAt": "2024-01-01T00:00:00Z",
            "thumbnailUrl": "https://example.com/thumb.jpg?Expires=9999999999",
            "contentUrl": "https://example.com/video.mp4",
        })
        assert media.id == "test-id"
        assert media.is_video is True
        assert media.thumbnail_url == "https://example.com/thumb.jpg?Expires=9999999999"
        assert media.content_url == "https://example.com/video.mp4"
        assert media.is_expired is False

    def test_old_media_without_new_fields(self):
        """Test that media without new fields still works (backward compatibility)."""
        media = Media({
            "__typename": "MediaVideo",
            "id": "test-id",
            "createdAt": "2024-01-01T00:00:00Z",
            "thumbnailUrl": "https://example.com/thumb.jpg",
            "contentUrl": "https://example.com/video.mp4",
        })
        # New fields should return None/False when missing
        assert media.quality is None
        assert media.state is None
        assert media.width is None
        assert media.height is None
        assert media.is_slow_motion is False
        assert media.is_ready is False
        assert media.dimensions is None
        assert media.aspect_ratio is None


class TestEdgeCases:
    """Tests for edge cases and error conditions."""

    def test_zero_dimensions(self):
        """Test handling of zero dimensions."""
        media = Media({
            "__typename": "MediaImage",
            "id": "test-id",
            "createdAt": "2024-01-01T00:00:00Z",
            "thumbnailUrl": "https://example.com/thumb.jpg",
            "width": 0,
            "height": 0,
        })
        assert media.width == 0
        assert media.height == 0
        assert media.dimensions == (0, 0)
        # aspect_ratio should be None for zero height to avoid division by zero
        assert media.aspect_ratio is None

    def test_only_width_provided(self):
        """Test when only width is provided."""
        media = Media({
            "__typename": "MediaImage",
            "id": "test-id",
            "createdAt": "2024-01-01T00:00:00Z",
            "thumbnailUrl": "https://example.com/thumb.jpg",
            "width": 1920,
        })
        assert media.width == 1920
        assert media.height is None
        assert media.dimensions is None
        assert media.aspect_ratio is None

    def test_only_height_provided(self):
        """Test when only height is provided."""
        media = Media({
            "__typename": "MediaImage",
            "id": "test-id",
            "createdAt": "2024-01-01T00:00:00Z",
            "thumbnailUrl": "https://example.com/thumb.jpg",
            "height": 1080,
        })
        assert media.width is None
        assert media.height == 1080
        assert media.dimensions is None
        assert media.aspect_ratio is None

    def test_string_dimensions_converted_to_int(self):
        """Test that string dimensions are converted to integers."""
        media = Media({
            "__typename": "MediaImage",
            "id": "test-id",
            "createdAt": "2024-01-01T00:00:00Z",
            "thumbnailUrl": "https://example.com/thumb.jpg",
            "width": "1920",
            "height": "1080",
        })
        assert media.width == 1920
        assert media.height == 1080
        assert isinstance(media.width, int)
        assert isinstance(media.height, int)
