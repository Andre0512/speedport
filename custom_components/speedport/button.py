from __future__ import annotations

from homeassistant.components.button import ButtonDeviceClass, ButtonEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import HomeAssistantType
from speedport import Speedport

from .const import DOMAIN
from .device import SpeedportEntity


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities(
        [
            SpeedportReconnectButton(hass, coordinator),
            SpeedportRebootButton(hass, coordinator),
            SpeedportWPSButton(hass, coordinator),
        ]
    )


class SpeedportReconnectButton(ButtonEntity, SpeedportEntity):
    _attr_device_class = ButtonDeviceClass.RESTART

    def __init__(self, hass: HomeAssistantType, speedport: Speedport) -> None:
        """Initialize the button entity."""
        super().__init__(hass, speedport)
        self._attr_name = "Reconnect"
        self._speedport = speedport
        self._attr_unique_id = "speedport_reconnect"

    async def async_press(self) -> None:
        """Send out a restart command."""
        await self._speedport.reconnect()


class SpeedportRebootButton(ButtonEntity, SpeedportEntity):
    _attr_device_class = ButtonDeviceClass.RESTART

    def __init__(self, hass: HomeAssistantType, speedport: Speedport) -> None:
        """Initialize the button entity."""
        super().__init__(hass, speedport)
        self._attr_name = "Reboot"
        self._speedport = speedport
        self._attr_unique_id = "speedport_reboot"

    async def async_press(self) -> None:
        """Send out a restart command."""
        await self._speedport.reboot()


class SpeedportWPSButton(ButtonEntity, SpeedportEntity):
    _attr_device_class = ButtonDeviceClass.IDENTIFY

    def __init__(self, hass: HomeAssistantType, speedport: Speedport) -> None:
        """Initialize the button entity."""
        super().__init__(hass, speedport)
        self._attr_name = "WPS on"
        self._speedport: Speedport = speedport
        self._attr_unique_id = "speedport_wps"

    async def async_press(self) -> None:
        """Send out a restart command."""
        await self._speedport.wps_on()
