"""Sensor platform for home-assistant-avocent-dpdu."""

from __future__ import annotations

from decimal import Decimal

from typing import TYPE_CHECKING

from homeassistant.components.sensor import (
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.const import UnitOfElectricCurrent
from .entity import PowerDistributionUnitCurrentEntity

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.entity_platform import AddEntitiesCallback

    from .coordinator import AvocentDpduDataUpdateCoordinator
    from .data import AvocentDPDUConfigEntry


ENTITY_DESCRIPTIONS = (
    SensorEntityDescription(
        key="home-assistant-avocent-dpdu",
        name="Combined Current",
        native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
        suggested_display_precision=1,
        state_class=SensorStateClass.MEASUREMENT,
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,  # noqa: ARG001 Unused function argument: `hass`
    entry: AvocentDPDUConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the sensor platform."""
    async_add_entities(
        AvocentDPDUSensorEntity(
            coordinator=entry.runtime_data.coordinator,
            entity_description=entity_description,
        )
        for entity_description in ENTITY_DESCRIPTIONS
    )


class AvocentDPDUSensorEntity(PowerDistributionUnitCurrentEntity, SensorEntity):
    """Avocent Direct PDU entity reporting overall status."""

    def __init__(
        self,
        coordinator: AvocentDpduDataUpdateCoordinator,
        entity_description: SensorEntityDescription,
    ) -> None:
        """Initialize the sensor class."""
        super().__init__(coordinator)
        self.entity_description = entity_description

    @property
    def should_poll(self) -> bool:
        """The AvocentDpduDataUpdateCoordinator will handle updates."""
        return False

    @property
    def native_value(self) -> Decimal:
        """Return the current value of the current sensor."""
        return Decimal(self.coordinator.api.get_current_deciamps()) / 10

    @property
    def icon(self) -> str:
        """Return a representative icon."""
        status = self.coordinator.api.get_pdu_status_integer()
        icon = "mdi:current-ac"  # Normal icon
        if status == 1:
            icon = "mdi:alert"  # Warning: approaching overload
        elif status == 2:
            icon = "mdi:electric-switch"  # Overloaded and turned off
        return icon
