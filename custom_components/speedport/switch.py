from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Set up entry."""

    speedport = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([SpeedportWifiSwitch(speedport)])


class SpeedportWifiSwitch(SwitchEntity):
    _attr_is_on: bool | None = False

    def __init__(self, speedport) -> None:
        self._description = "Wi-Fi"
        self._friendly_name = "Wi-Fi"
        self._icon = "mdi:wifi"
        self._type = "WiFiNetwork"

        self._name = f"{self._friendly_name} {self._description}"
        self._unique_id = self._description

        self._is_available = True
        self._speedport = speedport

    @property
    def name(self) -> str:
        """Return name."""
        return self._name

    @property
    def icon(self) -> str:
        """Return name."""
        return self._icon

    @property
    def unique_id(self) -> str:
        """Return unique id."""
        return self._unique_id

    @property
    def available(self) -> bool:
        """Return availability."""
        return True

    async def async_update(self) -> None:
        """Update data."""
        _LOGGER.debug("Updating '%s' (%s) switch state", self.name, self._type)
        # await self._update()

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn on switch."""
        await self._speedport.wifi_on()

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn off switch."""
        await self._speedport.wifi_off()

    async def _async_handle_turn_on_off(self, turn_on: bool) -> None:
        """Handle switch state change request."""
        # await self._switch(turn_on)
        self._attr_is_on = turn_on
