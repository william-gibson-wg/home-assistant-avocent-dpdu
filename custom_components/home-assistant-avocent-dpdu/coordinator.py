"""DataUpdateCoordinator for home-assistant-avocent-dpdu."""

from __future__ import annotations

from datetime import timedelta
from typing import TYPE_CHECKING, Any

from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from homeassistant.helpers.debounce import Debouncer
from homeassistant.const import CONF_HOST, CONF_PASSWORD, CONF_USERNAME

from .const import DOMAIN, LOGGER

from avocentdpdu.avocentdpdu import AvocentDPDU

if TYPE_CHECKING:
    from .data import AvocentDPDUConfigEntry
    from homeassistant.core import HomeAssistant


# https://developers.home-assistant.io/docs/integration_fetching_data#coordinated-single-api-poll-for-data-for-all-entities
class AvocentDpduDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching Avocent DPDU data from single endpoint."""

    def __init__(self, hass: HomeAssistant) -> None:
        """Initialize the coordinator."""
        config_entry: AvocentDPDUConfigEntry

        super().__init__(
            hass,
            LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=60),
            # Don't refresh immediately, give the device time to process
            # the change in state before we query it.
            request_refresh_debouncer=Debouncer(
                hass,
                LOGGER,
                cooldown=1.5,
                immediate=False,
            ),
        )

        LOGGER.debug("AvocentDpduDataUpdateCoordinator __init__:")
        LOGGER.debug(self.config_entry)

        self.api = AvocentDPDU(
            host=self.config_entry.data[CONF_HOST],
            username=self.config_entry.data[CONF_USERNAME],
            password=self.config_entry.data[CONF_PASSWORD],
            timeout=50,
        )

    async def _connect(self) -> None:
        """Connect to the Avocent DPDU."""
        LOGGER.debug("Initialize coordinator")
        await self.api.initialize()

    async def _async_update_data(self):
        """Fetch data from PDU."""
        LOGGER.debug("Update data request")
        await self.api.update()
