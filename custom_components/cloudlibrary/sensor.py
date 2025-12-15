"""CloudLibrary sensor platform for Home Assistant.

Defines sensors for patron data, library information, notifications, and user-specific metrics.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
import logging

from homeassistant.components.sensor import (
    RestoreSensor,
    SensorEntity,
    SensorEntityDescription,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import StateType

from . import CloudLibraryDataUpdateCoordinator
from .const import CONF_BARCODE, DOMAIN, MESSAGE_KEYS, PATRON_ITEM_KEYS
from .entity import CloudLibraryEntity

_LOGGER = logging.getLogger(__name__)


@dataclass
class CloudLibrarySensorDescription(SensorEntityDescription):
    """Sensor entity description for CloudLibrary."""

    available_fn: Callable | None = None
    value_fn: Callable | None = None
    attributes_fn: Callable | None = None
    entity_picture_fn: Callable | None = None
    unique_id_fn: Callable | None = None
    translation_key: str | None = None


SENSOR_TYPES: tuple[CloudLibrarySensorDescription, ...] = (
    CloudLibrarySensorDescription(
        key="featured",
        translation_key="user",
        unique_id_fn=lambda data: "user",
        icon="mdi:face-man",
        available_fn=lambda data: (data.get("display") or {}).get("patron") is not None,
        value_fn=lambda data: ((data.get("display") or {}).get("patron") or {}).get(
            "name"
        ),
        attributes_fn=lambda data: (data.get("display") or {}).get("patron"),
    ),
    CloudLibrarySensorDescription(
        key="email",
        translation_key="email",
        unique_id_fn=lambda data: "email",
        icon="mdi:email",
        available_fn=lambda data: (data.get("settings") is not None),
        value_fn=lambda data: (data.get("settings") or {}).get("email"),
        attributes_fn=lambda data: data.get("settings"),
    ),
    CloudLibrarySensorDescription(
        key="featured",
        translation_key="settings",
        unique_id_fn=lambda data: "settings",
        icon="mdi:cog",
        available_fn=lambda data: data.get("settings") is not None,
        value_fn=lambda data: len(data.get("settings") or []),
        attributes_fn=lambda data: data.get("settings"),
    ),
    CloudLibrarySensorDescription(
        key="featured",
        translation_key="notifications",
        unique_id_fn=lambda data: "notifications",
        icon="mdi:message-badge",
        available_fn=lambda data: data.get("notifications") is not None,
        value_fn=lambda data: (data.get("notifications") or {}).get("unreadCount"),
        attributes_fn=lambda data: {
            "messages": [
                {
                    **{
                        key: (
                            msg.get(key)
                            if key not in ("creationTime", "validUntilTime")
                            else msg.get(key, {}).get("time")
                        )
                        for key in MESSAGE_KEYS
                    },
                    "attachments": [
                        {
                            k: attachment.get(k)
                            for k in (
                                "title",
                                "isbn",
                                "publishedDate",
                                "imageLink",
                                "imageLinkThumbnail",
                                "mediaType",
                                "publisher",
                                "imageLinkCover",
                                "status",
                            )
                        }
                        for attachment in msg.get("objectAttachments", {}).values()
                    ],
                }
                for msg in (data.get("notifications") or {}).get("messages", [])
            ]
        },
    ),
    CloudLibrarySensorDescription(
        key="featured",
        translation_key="library",
        unique_id_fn=lambda data: "library",
        icon="mdi:library",
        available_fn=lambda data: (
            (data.get("config") or {}).get("libraryId") is not None
        ),
        value_fn=lambda data: (data.get("config") or {}).get("displayName"),
        attributes_fn=lambda data: {
            "supportEmail": (data.get("config") or {}).get("supportEmail"),
            "libraryCatalogUrl": (data.get("config") or {}).get("libraryCatalogUrl"),
            "maxLoanTimes": (
                (data.get("config") or {}).get("cloudLibraryConfiguration") or {}
            ).get("maxLoanTimes"),
            "maxLoanTimeUnit": (
                (data.get("config") or {}).get("cloudLibraryConfiguration") or {}
            ).get("maxLoanTimeUnit"),
            "maxLoanedDocuments": (
                (data.get("config") or {}).get("cloudLibraryConfiguration") or {}
            ).get("maxLoanedDocuments"),
            "maxHeldDocuments": (
                (data.get("config") or {}).get("cloudLibraryConfiguration") or {}
            ).get("maxHeldDocuments"),
            "allowRenewals": (data.get("config") or {}).get("allowRenewals"),
        },
    ),
    CloudLibrarySensorDescription(
        key="current",
        translation_key="current",
        unique_id_fn=lambda data: "current",
        icon="mdi:book-open-page-variant",
        available_fn=lambda data: (data.get("patronItems") is not None),
        value_fn=lambda data: len(data.get("patronItems") or []),
        attributes_fn=lambda data: {
            "patron_items": [
                {key: item.get(key) for key in PATRON_ITEM_KEYS}
                for item in data.get("patronItems") or []
            ]
        },
    ),
    CloudLibrarySensorDescription(
        key="holds",
        translation_key="holds",
        unique_id_fn=lambda data: "holds",
        icon="mdi:content-save-alert",
        available_fn=lambda data: (data.get("patronItems") is not None),
        value_fn=lambda data: len(data.get("patronItems") or []),
        attributes_fn=lambda data: {
            "patron_items": [
                {key: item.get(key) for key in PATRON_ITEM_KEYS}
                for item in data.get("patronItems") or []
            ]
        },
    ),
    CloudLibrarySensorDescription(
        key="saved",
        translation_key="saved",
        unique_id_fn=lambda data: "saved",
        icon="mdi:content-save-all",
        available_fn=lambda data: (data.get("patronItems") is not None),
        value_fn=lambda data: len(data.get("patronItems") or []),
        attributes_fn=lambda data: {
            "patron_items": [
                {key: item.get(key) for key in PATRON_ITEM_KEYS}
                for item in data.get("patronItems") or []
            ]
        },
    ),
    CloudLibrarySensorDescription(
        key="saved",
        translation_key="canborrow",
        unique_id_fn=lambda data: "canborrow",
        icon="mdi:book-check",
        available_fn=lambda data: (data.get("patronItems") is not None),
        value_fn=lambda data: len(
            [
                item
                for item in (data.get("patronItems") or [])
                if item.get("canBorrow") is True
            ]
        ),
        attributes_fn=lambda data: {
            "patron_items": [
                {key: item.get(key) for key in PATRON_ITEM_KEYS}
                for item in (data.get("patronItems") or [])
                if item.get("canBorrow") is True
            ]
        },
    ),
    CloudLibrarySensorDescription(
        key="history",
        translation_key="history",
        unique_id_fn=lambda data: "history",
        icon="mdi:bookshelf",
        available_fn=lambda data: (data.get("patronItems") is not None),
        value_fn=lambda data: len(data.get("patronItems") or []),
        attributes_fn=lambda data: {
            "patron_items": [
                {key: item.get(key) for key in PATRON_ITEM_KEYS}
                for item in data.get("patronItems") or []
            ]
        },
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the CloudLibrary sensors based on the coordinator's data."""
    _LOGGER.debug("[sensor|async_setup_entry] Starting sensor setup")

    coordinator: CloudLibraryDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id][
        "coordinator"
    ]
    device_name = entry.data[CONF_BARCODE]

    entities: list[CloudLibrarySensor] = []
    for sensor_type in SENSOR_TYPES:
        if sensor_type.key in coordinator.data:
            entities.append(CloudLibrarySensor(coordinator, sensor_type, device_name))

    async_add_entities(entities)


class CloudLibrarySensor(CloudLibraryEntity, RestoreSensor, SensorEntity):
    """Representation of a CloudLibrary sensor entity."""

    entity_description: CloudLibrarySensorDescription
    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: CloudLibraryDataUpdateCoordinator,
        description: CloudLibrarySensorDescription,
        device_name: str,
    ) -> None:
        """Initialize the CloudLibrary sensor entity."""
        super().__init__(coordinator, description, device_name)
        self.entity_id = f"sensor.{DOMAIN}_{self.entity_description.translation_key}"
        self._value: StateType = None

    @property
    def native_value(self) -> StateType:
        """Return the value reported by the sensor."""
        if self.coordinator.data is not None and self.entity_description.value_fn:
            return self.entity_description.value_fn(self.item)
        return self._value

    async def async_added_to_hass(self) -> None:
        """Restore state when entity is added to HA."""
        await super().async_added_to_hass()
        if self.coordinator.data is None:
            sensor_data = await self.async_get_last_sensor_data()
            if sensor_data is not None:
                _LOGGER.debug(f"Restoring latest data for {self.entity_id}")
                self._value = sensor_data.native_value
            else:
                _LOGGER.debug(f"Waiting for coordinator refresh for {self.entity_id}")
                await self.coordinator.async_request_refresh()
        else:
            self._value = (
                self.entity_description.value_fn(self.item)
                if self.entity_description.value_fn
                else None
            )

    @property
    def entity_picture(self) -> str | None:
        """Return the entity picture for the frontend, if any."""
        return (
            self.entity_description.entity_picture_fn(self.item)
            if self.entity_description.entity_picture_fn
            else None
        )

    @property
    def extra_state_attributes(self) -> dict:
        """Return additional state attributes for the sensor."""
        if not self.coordinator.data:
            return {}
        attributes = {"last_synced": self.last_synced}
        if self.entity_description.attributes_fn:
            fn_attrs = self.entity_description.attributes_fn(self.item) or {}
            attributes.update(fn_attrs)
        return attributes
