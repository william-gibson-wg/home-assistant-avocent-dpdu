"""Switch platform for home-assistant-avocent-dpdu."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from avocentdpdu.avocentdpdu import Outlet

from homeassistant.helpers.device_registry import format_mac

from homeassistant.components.switch import (
    SwitchEntity,
    SwitchEntityDescription,
    SwitchDeviceClass,
)

from .const import LOGGER

from .entity import PowerDistributionUnitOutletEntity

import asyncio

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.entity_platform import AddEntitiesCallback

    from .coordinator import AvocentDpduDataUpdateCoordinator
    from .data import AvocentDPDUConfigEntry


async def async_setup_entry(
    hass: HomeAssistant,  # noqa: ARG001 Unused function argument: `hass`
    entry: AvocentDPDUConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the switch platform."""
    async_add_entities(
        AvocentDpduSwitchEntity(
            outlet=outlet,
            coordinator=entry.runtime_data.coordinator,
            entity_description=SwitchEntityDescription(
                name=outlet.get_name(),
                key="home-assistant-avocent-dpdu",
                device_class=SwitchDeviceClass.OUTLET,
            ),
        )
        for outlet in entry.runtime_data.coordinator.api.switches()
    )


class AvocentDpduSwitchEntity(PowerDistributionUnitOutletEntity, SwitchEntity):
    """Avocent Direct PDU entity representing one outlet on a PDU of 8 or 16."""

    def __init__(
        self,
        coordinator: AvocentDpduDataUpdateCoordinator,
        entity_description: SwitchEntityDescription,
        outlet: Outlet,
    ) -> None:
        """Initialize the switch class."""
        super().__init__(coordinator)
        self.entity_description = entity_description

        self.outlet = outlet
        self.coordinator = coordinator

        self._attr_unique_id = f"{(coordinator.api.mac).rstrip()}-{outlet.get_name()}"

    @property
    def name(self) -> str:
        """Avocent name for this outlet."""
        return self.outlet.name

    @property
    def is_on(self) -> bool:
        """If the switch is currently on or off."""
        return self.outlet.is_on()

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn the switch on."""
        await self.outlet.turn_on()

        await asyncio.sleep(1)
        await self.coordinator.async_refresh()

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn the switch off."""
        await self.outlet.turn_off()

        await asyncio.sleep(1)
        await self.coordinator.async_refresh()
