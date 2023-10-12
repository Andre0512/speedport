from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import HomeAssistantType
from speedport import Speedport

from .const import DOMAIN
from .device import SpeedportEntity

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Set up entry."""

    speedport: Speedport = hass.data[DOMAIN][entry.entry_id]
    await speedport.update_status()
    async_add_entities(
        [
            SpeedportWifiSwitch(hass, speedport),
            SpeedportGuestWifiSwitch(hass, speedport),
            SpeedportOfficeWifiSwitch(hass, speedport),
        ]
    )


class SpeedportWifiSwitch(SwitchEntity, SpeedportEntity):
    _attr_is_on: bool | None = False

    def __init__(self, hass: HomeAssistantType, speedport: Speedport) -> None:
        super().__init__(hass, speedport)
        self._speedport: Speedport = speedport
        self._attr_icon = "mdi:wifi"
        self._attr_name = f"WLAN {speedport.wlan_ssid}"
        self._attr_unique_id = "wifi"

    @property
    def is_on(self) -> bool | None:
        return self._speedport.wlan_active

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn on switch."""
        await self._speedport.wifi_on()

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn off switch."""
        await self._speedport.wifi_off()


class SpeedportGuestWifiSwitch(SwitchEntity, SpeedportEntity):
    _attr_is_on: bool | None = False

    def __init__(self, hass: HomeAssistantType, speedport: Speedport) -> None:
        super().__init__(hass, speedport)
        self._speedport: Speedport = speedport
        self._attr_icon = "mdi:wifi"
        self._attr_name = f"WLAN {speedport.wlan_guest_ssid}"
        self._attr_unique_id = "wifi_guest"

    @property
    def is_on(self) -> bool | None:
        return self._speedport.wlan_guest_active

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn on switch."""
        await self._speedport.wifi_guest_on()

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn off switch."""
        await self._speedport.wifi_guest_off()


class SpeedportOfficeWifiSwitch(SwitchEntity, SpeedportEntity):
    _attr_is_on: bool | None = False

    def __init__(self, hass: HomeAssistantType, speedport: Speedport) -> None:
        super().__init__(hass, speedport)
        self._speedport: Speedport = speedport
        self._attr_icon = "mdi:wifi"
        self._attr_name = f"WLAN {speedport.wlan_office_ssid}"
        self._attr_unique_id = "wifi_office"

    @property
    def is_on(self) -> bool | None:
        return self._speedport.wlan_office_ssid

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn on switch."""
        await self._speedport.wifi_office_on()

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn off switch."""
        await self._speedport.wifi_office_off()
