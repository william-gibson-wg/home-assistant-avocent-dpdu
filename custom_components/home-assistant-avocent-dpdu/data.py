"""Custom types for home-assistant-avocent-dpdu."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry
    from homeassistant.loader import Integration

    from .coordinator import AvocentDpduDataUpdateCoordinator


type AvocentDPDUConfigEntry = ConfigEntry[AvocentDPDUData]


@dataclass
class AvocentDPDUData:
    """Data for the Avocent DPDU integration."""

    coordinator: AvocentDpduDataUpdateCoordinator
    integration: Integration
