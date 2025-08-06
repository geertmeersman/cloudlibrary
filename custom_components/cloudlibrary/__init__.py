"""CloudLibrary integration."""

from __future__ import annotations

from datetime import timedelta
import logging
from pathlib import Path

from aiocloudlibrary import CloudLibraryClient
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_SCAN_INTERVAL
from homeassistant.core import HomeAssistant
from homeassistant.helpers import device_registry as dr
from homeassistant.helpers.storage import STORAGE_DIR, Store
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from requests.exceptions import ConnectionError

from .const import (
    CONF_BARCODE,
    CONF_LIBRARY,
    CONF_PIN,
    DEFAULT_SCAN_INTERVAL,
    DOMAIN,
    PLATFORMS,
)
from .exceptions import (
    BadCredentialsException,
    CloudLibraryException,
    CloudLibraryServiceException,
)

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up CloudLibrary from a config entry."""
    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = {}

    for platform in PLATFORMS:
        hass.data[DOMAIN][entry.entry_id].setdefault(platform, set())

    client = CloudLibraryClient(
        barcode=entry.data[CONF_BARCODE],
        pin=entry.data[CONF_PIN],
        library=entry.data[CONF_LIBRARY],
    )

    storage_dir = Path(f"{hass.config.path(STORAGE_DIR)}/{DOMAIN}")
    if storage_dir.is_file():
        storage_dir.unlink()
    storage_dir.mkdir(exist_ok=True)
    store: Store = Store(hass, 1, f"{DOMAIN}/{entry.entry_id}")
    dev_reg = dr.async_get(hass)
    hass.data[DOMAIN][entry.entry_id]["coordinator"] = coordinator = (
        CloudLibraryDataUpdateCoordinator(
            hass,
            config_entry=entry,
            dev_reg=dev_reg,
            client=client,
            store=store,
        )
    )

    await coordinator.async_config_entry_first_refresh()

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""

    # Unload the platforms first
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        hass.data[DOMAIN].pop(entry.entry_id)

        # Define blocking file operations
        def remove_storage_files():
            storage = Path(f"{hass.config.path(STORAGE_DIR)}/{DOMAIN}/{entry.entry_id}")
            storage.unlink(missing_ok=True)  # Unlink (delete) the storage file

            storage_dir = Path(f"{hass.config.path(STORAGE_DIR)}/{DOMAIN}")
            # If the directory exists and is empty, remove it
            # If the directory exists and is empty, remove it
            if storage_dir.is_dir():
                try:
                    if not any(storage_dir.iterdir()):
                        storage_dir.rmdir()
                except Exception as e:
                    _LOGGER.warning(f"Could not remove directory {storage_dir}: {e}")

        # Offload the file system operations to a thread
        await hass.async_add_executor_job(remove_storage_files)

    return unload_ok


class CloudLibraryDataUpdateCoordinator(DataUpdateCoordinator):
    """Data update coordinator for CloudLibrary."""

    def __init__(
        self,
        hass: HomeAssistant,
        config_entry: ConfigEntry,
        dev_reg: dr.DeviceRegistry,
        client: CloudLibraryClient,
        store: Store,
    ) -> None:
        """Initialize coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(minutes=config_entry.data[CONF_SCAN_INTERVAL]),
            config_entry=config_entry,
        )
        self._debug = _LOGGER.isEnabledFor(logging.DEBUG)
        self._config_entry = config_entry
        self._device_registry = dev_reg
        self.hass = hass
        self.client = client
        self.store = store

    async def async_config_entry_first_refresh(self) -> None:
        """Refresh data for the first time when a config entry is setup."""
        self.data = await self.store.async_load() or {}
        _LOGGER.debug("Loading store data")
        await super().async_config_entry_first_refresh()

    async def get_data(self) -> dict | None:
        """Get the data from the cloudLibrary client."""

        tasks = ["featured", "current", "holds", "saved", "history", "email"]

        self.data = {key: await getattr(self.client, key)() for key in tasks}

        await self.store.async_save(self.data)

    async def _async_update_data(self) -> dict | None:
        """Update data."""
        _LOGGER.debug("Updating data")
        if self._debug:
            await self.get_data()
        else:
            try:
                await self.get_data()
            except ConnectionError as exception:
                raise UpdateFailed(f"ConnectionError {exception}") from exception
            except BadCredentialsException as exception:
                raise UpdateFailed(
                    f"BadCredentialsException {exception}"
                ) from exception
            except CloudLibraryServiceException as exception:
                raise UpdateFailed(
                    f"CloudLibraryServiceException {exception}"
                ) from exception
            except CloudLibraryException as exception:
                raise UpdateFailed(f"CloudLibraryException {exception}") from exception
            except Exception as exception:
                raise UpdateFailed(f"Exception {exception}") from exception

        if len(self.data) > 0:
            return self.data
        return {}


async def async_migrate_entry(hass: HomeAssistant, config_entry: ConfigEntry) -> bool:
    """Migrate old entry."""
    _LOGGER.info("Migrating from version %s", config_entry.version)

    if config_entry.version == 1:
        new = {**config_entry.data}
        # TODO: modify Config Entry data
        if CONF_SCAN_INTERVAL not in new:
            new[CONF_SCAN_INTERVAL] = DEFAULT_SCAN_INTERVAL

        config_entry.version = 2
        hass.config_entries.async_update_entry(config_entry, data=new)

    _LOGGER.info("Migration to version %s successful", config_entry.version)

    return True
