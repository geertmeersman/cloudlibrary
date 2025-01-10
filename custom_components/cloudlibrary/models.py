"""Models used by CloudLibrary."""

from __future__ import annotations

from typing import TypedDict


class CloudLibraryConfigEntryData(TypedDict):
    """Config entry for the CloudLibrary integration."""

    barcode: str | None
    pin: str | None
    library: str | None
