import logging

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
    BinarySensorEntityDescription,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from speedport import Speedport

from .const import DOMAIN
from .device import SpeedportEntity

_LOGGER = logging.getLogger(__name__)

BINARY_SENSORS: tuple[BinarySensorEntityDescription, ...] = (
    BinarySensorEntityDescription(
        key="onlinestatus",
        name="Connection",
        device_class=BinarySensorDeviceClass.CONNECTIVITY,
    ),
    BinarySensorEntityDescription(
        key="dsl_link_status",
        name="DSL-Connection",
        device_class=BinarySensorDeviceClass.PLUG,
    ),
)


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Set up entry."""
    speedport: Speedport = hass.data[DOMAIN][entry.entry_id]

    entities = [
        SpeedportBinarySensor(hass, speedport, description)
        for description in BINARY_SENSORS
    ]

    async_add_entities(entities)


class SpeedportBinarySensor(SpeedportEntity, BinarySensorEntity):
    entity_description: BinarySensorEntityDescription

    @property
    def is_on(self) -> bool | None:
        """Return true if the binary sensor is on."""
        return self._speedport.get(self.entity_description.key) == "online"

    def available(self) -> bool:
        if self._speedport.get(self.entity_description.key) is None:
            return False
        return super().available
