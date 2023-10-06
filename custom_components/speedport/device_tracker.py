from __future__ import annotations

from homeassistant.components.device_tracker import ScannerEntity, SourceType
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from speedport.device import WlanDevice

from .const import DOMAIN


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    coordinator = hass.data[DOMAIN][entry.entry_id]
    devices = [SpeedportTracker(device) for device in await coordinator.devices]
    async_add_entities(devices)


class SpeedportTracker(ScannerEntity):
    _attr_should_poll = False

    def __init__(self, device: WlanDevice) -> None:
        super().__init__()
        self._device = device
        self._attr_unique_id = device.mac
        self._attr_name = device.name

    @property
    def source_type(self) -> SourceType:
        """Return the source type."""
        return SourceType.ROUTER

    @property
    def hostname(self) -> str | None:
        """Return the hostname of device."""
        return self._device.name

    @property
    def ip_address(self) -> str | None:
        """Return the primary ip address of the device."""
        return self._device.ipv4

    @property
    def is_connected(self) -> bool:
        """Return device status."""
        return self._device.connected

    @property
    def mac_address(self) -> str:
        """Return mac_address."""
        return self._device.mac

    @property
    def icon(self) -> str:
        """Return device icon."""
        if self.is_connected:
            return "mdi:lan-connect"
        return "mdi:lan-disconnect"

    @property
    def extra_state_attributes(self) -> dict[str, str]:
        """Return the attributes."""
        attrs: dict[str, str] = {}
        attrs["downspeed"] = self._device.downspeed
        attrs["fix_dhcp"] = self._device.fix_dhcp
        attrs["gua_ipv6"] = self._device.gua_ipv6
        attrs["hasui"] = self._device.hasui
        attrs["reservedip"] = self._device.reservedip
        attrs["rssi"] = self._device.rssi
        attrs["slave"] = self._device.slave
        attrs["type"] = self._device.type
        attrs["ula_ipv6"] = self._device.ula_ipv6
        attrs["upspeed"] = self._device.upspeed
        attrs["use_dhcp"] = self._device.use_dhcp
        attrs["wifi"] = self._device.wifi
        attrs["id"] = self._device.id
        return attrs

    @property
    def name(self) -> str:
        """Return device name."""
        return self._device.name
