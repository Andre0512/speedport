from __future__ import annotations

import logging
from datetime import timedelta

from homeassistant.components.device_tracker import ScannerEntity, SourceType
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
)
from speedport import Speedport
from speedport.device import WlanDevice

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    speedport = hass.data[DOMAIN][entry.entry_id]
    coordinator = SpeedportCoordinator(hass, speedport)
    await coordinator.async_config_entry_first_refresh()
    devices = [SpeedportTracker(coordinator, mac) for mac in await speedport.devices]
    async_add_entities(devices)


class SpeedportCoordinator(DataUpdateCoordinator):
    def __init__(self, hass: HomeAssistant, api: Speedport):
        """Initialize my coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            name="Speedport",
            update_interval=timedelta(seconds=10),
        )
        self._api: Speedport = api

    async def _async_update_data(self):
        return await self._api.devices


class SpeedportTracker(CoordinatorEntity, ScannerEntity):
    def __init__(self, coordinator: SpeedportCoordinator, mac: str) -> None:
        super().__init__(coordinator)
        self._mac = mac
        self._device: WlanDevice = self.coordinator.data.get(mac)

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

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self._device = self.coordinator.data.get(self._mac)
        self.async_write_ha_state()
