"""Base CloudLibrary entity for Home Assistant.

Defines the CloudLibraryEntity class as a base for all sensor entities.
"""

from __future__ import annotations

from datetime import datetime
import logging

from homeassistant.core import callback
from homeassistant.helpers.device_registry import DeviceEntryType
from homeassistant.helpers.entity import DeviceInfo, EntityDescription
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from . import CloudLibraryDataUpdateCoordinator
from .const import ATTRIBUTION, DOMAIN, NAME, VERSION, WEBSITE

_LOGGER = logging.getLogger(__name__)


class CloudLibraryEntity(CoordinatorEntity[CloudLibraryDataUpdateCoordinator]):
    """Base CloudLibrary entity using a coordinator."""

    _attr_attribution = ATTRIBUTION
    _unrecorded_attributes = frozenset({"patron_items", "messages", "last_synced"})

    def __init__(
        self,
        coordinator: CloudLibraryDataUpdateCoordinator,
        description: EntityDescription,
        device_name: str,
    ) -> None:
        """Initialize the CloudLibrary entity."""
        super().__init__(coordinator)
        self.entity_description = description
        self._identifier = f"{description.key}"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, f"{coordinator.config_entry.entry_id}")},
            name=f"{NAME} {device_name}",
            manufacturer=NAME,
            configuration_url=WEBSITE,
            entry_type=DeviceEntryType.SERVICE,
            sw_version=VERSION,
        )
        self._attr_unique_id = f"{coordinator.config_entry.entry_id}_{self.entity_description.translation_key}_{self.entity_description.unique_id_fn(self.item)}"
        self.last_synced = datetime.now()
        _LOGGER.debug(f"[CloudLibraryEntity|init] {self._identifier}")

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        if self.entity_description.key in self.coordinator.data:
            self.last_synced = datetime.now()
            self.async_write_ha_state()
        else:
            _LOGGER.debug(
                f"[CloudLibraryEntity|_handle_coordinator_update] "
                f"{self._attr_unique_id}: async_write_ha_state ignored, data missing"
            )

    @property
    def item(self) -> dict:
        """Return the coordinator data for this entity."""
        return self.coordinator.data.get(self.entity_description.key, {})

    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        try:
            return super().available and (
                self.entity_description.available_fn(self.item)
                if self.entity_description.available_fn
                else True
            )
        except Exception as e:
            _LOGGER.warning(
                "Error checking availability for %s: %s", self._attr_unique_id, e
            )
            return False

    async def async_update(self) -> None:
        """Update the entity.

        This method is a no-op because updates are handled via the coordinator.
        """
        return
