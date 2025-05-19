from enum import IntEnum


class MissedWastePickupStatusEnum(IntEnum):
    """Enum for missed waste pickup status."""

    PENDING_REVIEW = 0
    REVIEWED = 1
