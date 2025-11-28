"""Bird Buddy feeder models and device information.

This module provides classes for interacting with Bird Buddy feeder devices,
including device state, battery and signal metrics, power profiles, and
video capabilities.
"""

from collections import UserDict
from enum import Enum

from . import LOGGER


class MetricState(Enum):
    """Feeder metric states for battery, signal strength, and food level.

    Represents the state of various feeder metrics as reported by the API.

    Values:
        LOW: Metric is in low state (e.g., low battery, weak signal)
        MEDIUM: Metric is in medium state
        HIGH: Metric is in high state (e.g., full battery, strong signal)
        UNKNOWN: Metric state could not be determined
    """

    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"

    UNKNOWN = "UNKNOWN"

    @classmethod
    def _missing_(cls, value: str):
        LOGGER.warning("Unexpected metric state: %s", value)
        return MetricState.UNKNOWN


class PowerProfile(Enum):
    """Feeder power profiles controlling detection frequency and battery usage.

    Power profiles determine how frequently the feeder checks for bird activity,
    balancing detection sensitivity with battery life.

    Values:
        FRENZY: Maximum detection frequency (requires active subscription)
        STANDARD: Normal detection frequency (default)
        POWER_SAVE: Reduced detection frequency for extended battery life
        UNKNOWN: Profile could not be determined
    """

    FRENZY = "FRENZY_MODE"
    POWER_SAVE = "POWER_SAVER_MODE"
    STANDARD = "STANDARD_MODE"

    UNKNOWN = "UNKNOWN"

    @classmethod
    def _missing_(cls, value: str):
        LOGGER.warning("Unexpected power profile: %s", value)
        return PowerProfile.UNKNOWN


class FeederState(Enum):
    """Current operational state of a Bird Buddy feeder.

    Represents the various states a feeder can be in, from online operation
    to offline modes and maintenance states.

    Values:
        ONLINE: Feeder is online and operational
        OFFLINE: Feeder is not connected to the network
        OFF_GRID: Feeder is in off-grid mode (manual activation required)
        STREAMING: Feeder is actively streaming video
        READY_TO_STREAM: Feeder is ready to begin streaming
        TAKING_POSTCARDS: Feeder is capturing bird photos/videos
        FIRMWARE_UPDATE: Feeder is updating firmware
        DEEP_SLEEP: Feeder is in deep sleep mode
        FACTORY_RESET: Feeder is performing factory reset
        PENDING_FACTORY_RESET: Factory reset is queued
        PENDING_REMOVAL: Feeder removal is pending
        OUT_OF_FEEDER: No feeder detected (removed from network)
        UNKNOWN: State could not be determined
    """

    DEEP_SLEEP = "DEEP_SLEEP"
    FACTORY_RESET = "FACTORY_RESET"
    FIRMWARE_UPDATE = "FIRMWARE_UPDATE"
    OFFLINE = "OFFLINE"
    OFF_GRID = "OFF_GRID"
    ONLINE = "ONLINE"
    OUT_OF_FEEDER = "OUT_OF_FEEDER"
    PENDING_FACTORY_RESET = "PENDING_FACTORY_RESET"
    PENDING_REMOVAL = "PENDING_REMOVAL"
    READY_TO_STREAM = "READY_TO_STREAM"
    STREAMING = "STREAMING"
    TAKING_POSTCARDS = "TAKING_POSTCARDS"

    UNKNOWN = "UNKNOWN"

    @classmethod
    def _missing_(cls, value: str):
        LOGGER.warning("Unexpected feeder.state: %s", value)
        return FeederState.UNKNOWN


class Signal(UserDict[str, any]):
    """WiFi signal strength metrics for a feeder.

    Provides access to signal strength (RSSI) and quality state.

    Examples:
        >>> signal = feeder.signal
        >>> signal.rssi
        -45
        >>> signal.state
        <MetricState.HIGH: 'HIGH'>
    """

    @property
    def rssi(self) -> int:
        """Signal strength."""
        return self.get("value", -1)

    @property
    def state(self) -> MetricState:
        """Signal strength."""
        return MetricState(self.get("state", "UNKNOWN"))


class Battery(UserDict[str, any]):
    """Battery status and charge information for a feeder.

    Provides battery percentage, charging status, and battery health state.

    Examples:
        >>> battery = feeder.battery
        >>> battery.percentage
        85
        >>> battery.is_charging
        False
        >>> battery.state
        <MetricState.HIGH: 'HIGH'>
    """

    @property
    def percentage(self) -> int:
        """Percentage of battery remaining."""
        return self.get("percentage", 0)

    @property
    def is_charging(self) -> bool:
        """Whether the battery is charging."""
        return self.get("charging", False)

    @property
    def state(self) -> MetricState:
        """The state (low, medium, high) of the battery."""
        return MetricState(self.get("state", "UNKNOWN"))


class Feeder(UserDict[str, any]):
    """Represents a Bird Buddy smart feeder device with full configuration and status.

    The Feeder class provides access to all device information including battery status,
    WiFi signal strength, firmware version, housing type, video capabilities, and
    operational state. It supports both owner and shared feeder access with
    appropriate permission restrictions.

    The class inherits from UserDict, so all dictionary operations are supported.
    Use the provided properties for typed access to device information.

    Examples:
        >>> feeder = bb.feeders["feeder-uuid"]
        >>> print(f"{feeder.name}: {feeder.state}")
        'Backyard Buddy: FeederState.ONLINE'

        >>> print(f"Battery: {feeder.battery.percentage}%")
        'Battery: 85%'

        >>> if feeder.supports_audio:
        ...     print(f"Audio enabled: {feeder.is_audio_enabled}")
        'Audio enabled: True'

        >>> print(f"Device: {feeder.housing_type} v{feeder.device_version}")
        'Device: STANDARD v2.0'

    Attributes:
        All feeder data is stored in the underlying dictionary.
        Use properties for typed access to standard fields.

    Note:
        Some properties are only available to the feeder owner and will
        return None for shared feeders. Check is_owner before accessing
        owner-only properties like video_quality or version_update_available.
    """

    def __str__(self):
        """Return a string representation of the Feeder."""
        return f"<Feeder: {self.name}, {self.state}, " f"{self.battery.percentage}%>"

    @property
    def id(self):
        """UUID."""
        return self["id"]

    @property
    def serial(self):
        """Feeder SN."""
        return self["serialNumber"]

    @property
    def name(self):
        """Feeder name, as set in the app."""
        return self.get("name", "Bird Buddy")

    @property
    def is_owner(self):
        """Whether the logged in user is the owner of this feeder."""
        return self.get("__typename") == "FeederForOwner"

    @property
    def is_pending(self):
        """``True`` if waiting for the owner account to approve access to the Feeder."""
        return self.get("__typename") == "FeederForMemberPending"

    @property
    def is_public(self):
        """Whether this is a public feeder."""
        return self.get("__typename") == "FeederForPublic"

    @property
    def housing_type(self) -> str | None:
        """Feeder housing type/model, or None if not available."""
        return self.get("housingType")

    @property
    def device_version(self) -> str | None:
        """Device hardware/firmware version, or None if not available."""
        return self.get("version")

    @property
    def version(self) -> str:
        """Firmware version (owner only), or device version if available."""
        # Try firmwareVersion first (owner-only field), then version field
        return self.get("firmwareVersion") or self.get("version")

    @property
    def version_update_available(self) -> str:
        """Firmware update version (owner only)."""
        return self.get("availableFirmwareVersion", None)

    @property
    def state(self) -> FeederState:
        """State of the Feeder."""
        return FeederState(self.get("state", "UNKNOWN"))

    @property
    def is_off_grid(self) -> bool:
        """Whether `state` is `FeederState.OFF_GRID`."""
        return self.get("offGrid", None)

    @property
    def is_audio_enabled(self) -> bool:
        """Whether videos will contain audio."""
        return self.get("audioEnabled", None)

    @property
    def supports_audio(self) -> bool | None:
        """Whether the feeder supports audio recording, or None if not available."""
        return self.get("supportsAudio")

    @property
    def supports_enhanced_livestream(self) -> bool | None:
        """Whether the feeder supports enhanced livestream, or None if not available."""
        return self.get("supportsEnhancedLivestream")

    @property
    def supports_webrtc(self) -> bool | None:
        """Whether the feeder supports WebRTC, or None if not available."""
        return self.get("supportsWebRTC")

    @property
    def video_high_quality_enabled(self) -> bool | None:
        """Whether high quality video is enabled (owner only), or None if not available."""
        return self.get("videoHighQualityEnabled")

    @property
    def video_quality(self) -> str | None:
        """Video quality setting (owner only), or None if not available."""
        return self.get("videoQuality")

    @property
    def owner(self) -> str:
        """The username who first paired the Feeder."""
        return self.get("ownerName")

    @property
    def battery(self) -> Battery:
        """Battery metrics."""
        return Battery(self.get("battery", {}))

    @property
    def signal(self) -> Signal:
        """(wifi) signal metrics."""
        return Signal(self.get("signal", {}))

    @property
    def location(self) -> tuple[str | None, str | None]:
        """Configured location of the Feeder."""
        return (self.get("locationCity"), self.get("locationCountry"))

    @property
    def frequency(self) -> MetricState:
        """Configured frequency of the Feeder."""
        LOGGER.warning("Feeder.frequency is deprecated. Use power_profile instead")
        return MetricState(self.get("frequency", "UNKNOWN"))

    @property
    def power_profile(self) -> PowerProfile:
        """Configured power profile of the Feeder."""
        return PowerProfile(self.get("powerProfile", "STANDARD"))

    @property
    # @incubating
    def food(self) -> MetricState:
        """Level of bird seed in the feeder.

        @incubating This field appears not to work currently.
        """
        LOGGER.debug("birdbuddy.Feeder.food is incubating")
        return MetricState(self.get("food", {}).get("state", "UNKNOWN"))

    @property
    # @incubating
    def temperature(self) -> int:
        """Temperature at the feeder.

        @incubating This field appears not to work currently.
        """
        LOGGER.debug("birdbuddy.Feeder.temperature is incubating")
        return self.get("temperature", {}).get("value", 0)


class FeederUpdateStatus(UserDict[str, any]):
    """Status of a feeder firmware update operation.

    Tracks the progress and outcome of firmware updates initiated through
    the API. Use the is_complete, is_in_progress, and is_failed properties
    to check update status.

    Examples:
        >>> status = await bb.update_firmware_start(feeder)
        >>> if status.is_in_progress:
        ...     print(f"Update progress: {status.progress}%")
        >>> elif status.is_complete:
        ...     print("Update completed successfully")
        >>> elif status.is_failed:
        ...     print(f"Update failed: {status.failure_reason}")
    """

    @property
    def feeder(self) -> Feeder:
        """Returns a partial Feeder result."""
        return Feeder(self["feeder"])

    @property
    def is_complete(self) -> bool:
        """`True` if the firmware update was successfully completed."""
        return self["__typename"] == "FeederFirmwareUpdateSucceededResult"

    @property
    def is_in_progress(self) -> bool:
        """`True` if the firmware update is in progress."""
        return (
            self["__typename"] == "FeederFirmwareUpdateProgressResult"
            and self.get("progress", None) is not None
        )

    @property
    def is_failed(self) -> bool:
        """`True` if the firmware update has failed."""
        return self["__typename"] == "FeederFirmwareUpdateFailedResult"

    @property
    def failure_reason(self) -> str:
        """Failure reason, or `None` if no failure."""
        return self.get("failedReason", None)

    @property
    def progress(self) -> int:
        """Current firmware installation progress."""
        return self.get("progress", None)
