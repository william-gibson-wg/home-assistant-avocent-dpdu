"""BlueprintEntity class."""

from __future__ import annotations

from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .coordinator import AvocentDpduDataUpdateCoordinator


class PowerDistributionUnitOutletEntity(
    CoordinatorEntity[AvocentDpduDataUpdateCoordinator]
):
    """Define an Outlet entity."""

    def __init__(self, coordinator: AvocentDpduDataUpdateCoordinator) -> None:
        """Initialize."""
        super().__init__(coordinator)
        self._attr_unique_id = coordinator.config_entry.entry_id
        self._attr_device_info = DeviceInfo(
            identifiers={
                (
                    coordinator.config_entry.domain,
                    coordinator.config_entry.entry_id,
                ),
            },
            manufacturer="Avocent",
            model="DPDU",
            name="DPDU",
            sw_version="1.2.0",
        )


class PowerDistributionUnitCurrentEntity(
    CoordinatorEntity[AvocentDpduDataUpdateCoordinator]
):
    """Define an current sensor entity."""

    def __init__(self, coordinator: AvocentDpduDataUpdateCoordinator) -> None:
        """Initialize."""
        super().__init__(coordinator)
        self._attr_unique_id = coordinator.config_entry.entry_id
        self._attr_device_info = DeviceInfo(
            identifiers={
                (
                    coordinator.config_entry.domain,
                    coordinator.config_entry.entry_id,
                ),
            },
            manufacturer="Avocent",
            model="DPDU10x/20x",
            name="DPDU",
            sw_version="1.2.0",
        )
