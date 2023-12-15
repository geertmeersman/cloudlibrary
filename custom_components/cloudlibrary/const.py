"""Constants used by CloudLibrary."""
import json
from pathlib import Path
from typing import Final

from homeassistant.const import Platform

PLATFORMS: Final = [Platform.SENSOR]

ATTRIBUTION: Final = "Data provided by cloudLibrary"

DEFAULT_SCAN_INTERVAL = 15
SCAN_INTERVAL_MIN = 10
SCAN_INTERVAL_MAX = 1440
CONF_BARCODE = "barcode"
CONF_PIN = "pin"
CONF_LIBRARY = "library"
MESSAGE_KEYS = ["read", "creationTime", "subject", "validUntilTime", "text"]
PATRON_ITEM_KEYS = [
    "title",
    "contributors",
    "borrowedDate",
    "dueDate",
    "returnedDate",
    "holdAvailableDate",
    "holdExpiresDate",
    "holdQueuePosition",
    "isHoldAvailable",
    "isbn",
    "imageLink",
    "mediaCategory",
    "mediaType",
    "state",
    "publishedDate",
    "canFavorite",
    "canReturn",
    "canBorrow",
    "canRenew",
    "canHold",
    "canRemoveHold",
    "canSave",
    "canRead",
    "canListen",
    "canBag",
    "canHide",
    "isFavorite",
    "isHeld",
]
WEBSITE = "https://www.yourcloudlibrary.com/"

manifestfile = Path(__file__).parent / "manifest.json"
with open(manifestfile) as json_file:
    manifest_data = json.load(json_file)

DOMAIN = manifest_data.get("domain")
NAME = manifest_data.get("name")
VERSION = manifest_data.get("version")
ISSUEURL = manifest_data.get("issue_tracker")
STARTUP = f"""
-------------------------------------------------------------------
{NAME}
Version: {VERSION}
This is a custom component
If you have any issues with this you need to open an issue here:
{ISSUEURL}
-------------------------------------------------------------------
"""
