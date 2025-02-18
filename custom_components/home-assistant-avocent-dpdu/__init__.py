"""
Custom integration to integrate home-assistant-avocent-dpdu with Home Assistant.

For more details about this integration, please refer to
https://github.com/william-gibson-wg/home-assistant-avocent-dpdu
"""

from __future__ import annotations
from dataclasses import dataclass

from datetime import timedelta
from typing import TYPE_CHECKING

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.helpers import device_registry as dr

# from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.loader import async_get_loaded_integration


from .const import DOMAIN, LOGGER
from .coordinator import AvocentDpduDataUpdateCoordinator
from .data import AvocentDPDUData

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant

    from .data import AvocentDPDUConfigEntry

PLATFORMS: list[Platform] = [
    Platform.SENSOR,
    Platform.SWITCH,
]


# https://developers.home-assistant.io/docs/config_entries_index/#setting-up-an-entry
async def async_setup_entry(
    hass: HomeAssistant,
    entry: AvocentDPDUConfigEntry,
) -> bool:
    """Set up Avocent Direct PDU from a config entry."""
    coordinator = AvocentDpduDataUpdateCoordinator(hass=hass)
    entry.runtime_data = AvocentDPDUData(
        integration=async_get_loaded_integration(hass, entry.domain),
        coordinator=coordinator,
    )

    # https://developers.home-assistant.io/docs/integration_fetching_data#coordinated-single-api-poll-for-data-for-all-entities
    await coordinator.async_config_entry_first_refresh()

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    entry.async_on_unload(entry.add_update_listener(async_reload_entry))

    return True


async def async_unload_entry(
    hass: HomeAssistant,
    entry: AvocentDPDUConfigEntry,
) -> bool:
    """Handle removal of an entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)


async def async_reload_entry(
    hass: HomeAssistant,
    entry: AvocentDPDUConfigEntry,
) -> None:
    """Reload config entry."""
    await async_unload_entry(hass, entry)
    await async_setup_entry(hass, entry)
