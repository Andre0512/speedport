from __future__ import annotations

from homeassistant.components.button import ButtonDeviceClass, ButtonEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import EntityCategory
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities(
        [
            SpeedportReconnectButton(coordinator),
            SpeedportRebootButton(coordinator),
        ]
    )


class SpeedportReconnectButton(ButtonEntity):
    _attr_device_class = ButtonDeviceClass.RESTART
    _attr_entity_category = EntityCategory.CONFIG
    _attr_name = "Reconnect"

    def __init__(self, coordinator) -> None:
        """Initialize the button entity."""
        self.coordinator = coordinator
        self._attr_unique_id = "speedport_reconnect"

    async def async_press(self) -> None:
        """Send out a restart command."""
        await self.coordinator.reconnect()


class SpeedportRebootButton(ButtonEntity):
    _attr_device_class = ButtonDeviceClass.RESTART
    _attr_entity_category = EntityCategory.CONFIG
    _attr_name = "Reboot"

    def __init__(self, coordinator) -> None:
        """Initialize the button entity."""
        self.coordinator = coordinator
        self._attr_unique_id = "speedport_reboot"

    async def async_press(self) -> None:
        """Send out a restart command."""
        await self.coordinator.reboot()
