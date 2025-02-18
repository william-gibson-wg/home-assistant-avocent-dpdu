"""Constants for home-assistant-avocent-dpdu."""

from logging import Logger, getLogger
from typing import Final

LOGGER: Logger = getLogger(__package__)

DOMAIN = "home-assistant-avocent-dpdu"

DEFAULT_USERNAME: Final = "snmp"
DEFAULT_PASSWORD: Final = "1234"  # noqa: S105
