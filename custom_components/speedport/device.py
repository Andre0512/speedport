import asyncio
import logging
from datetime import timedelta

from homeassistant.core import callback
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.typing import HomeAssistantType
from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    CoordinatorEntity,
)
from speedport import Speedport

from .const import DOMAIN, UPDATE_INTERVAL

_LOGGER = logging.getLogger(__name__)


class SpeedportCoordinator(DataUpdateCoordinator[None]):
    def __init__(self, hass: HomeAssistantType, device: Speedport):
        """Initialize my coordinator."""

        super().__init__(
            hass,
            _LOGGER,
            name=device.device_name,
            update_interval=timedelta(seconds=UPDATE_INTERVAL),
        )
        self._speedport: Speedport = device

    async def _async_update_data(self) -> None:
        await asyncio.gather(
            *[self._speedport.update_status(), self._speedport.update_ip_data()]
        )


class SpeedportEntity(CoordinatorEntity[SpeedportCoordinator]):
    _attr_has_entity_name = True

    def __init__(
        self, hass: HomeAssistantType, speedport: Speedport, description=None
    ) -> None:
        coordinator = get_coordinator(hass, speedport)
        super().__init__(coordinator)

        self._coordinator = coordinator
        self._speedport: Speedport = speedport
        if description is not None:
            self.entity_description = description
            self._attr_unique_id = f"speedport_{description.key}"

    @property
    def device_info(self) -> DeviceInfo:
        return DeviceInfo(
            identifiers={(DOMAIN, self._speedport.serial_number)},
            manufacturer="Telekom",
            name="Speedport",
            model=self._speedport.device_name,
            sw_version=self._speedport.firmware_version,
            configuration_url=self._speedport.api.url,
        )

    @callback
    def _handle_coordinator_update(self) -> None:
        self.async_write_ha_state()


def get_coordinator(
    hass: HomeAssistantType, speedport: Speedport
) -> SpeedportCoordinator:
    coordinators = hass.data[DOMAIN]["coordinators"]
    if speedport.serial_number in coordinators:
        coordinator: SpeedportCoordinator = hass.data[DOMAIN]["coordinators"][
            speedport.serial_number
        ]
    else:
        coordinator = SpeedportCoordinator(hass, speedport)
        hass.data[DOMAIN]["coordinators"][speedport.serial_number] = coordinator
    return coordinator
