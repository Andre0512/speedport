import logging
from dataclasses import dataclass

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


@dataclass
class SpeedportBinarySensorEntityDescription(BinarySensorEntityDescription):
    condition_key: str = ""
    value: str = ""


BINARY_SENSORS: tuple[SpeedportBinarySensorEntityDescription, ...] = (
    SpeedportBinarySensorEntityDescription(
        key="onlinestatus",
        name="Connection",
        device_class=BinarySensorDeviceClass.CONNECTIVITY,
        value="online",
    ),
    SpeedportBinarySensorEntityDescription(
        key="dsl_link_status",
        name="DSL-Connection",
        device_class=BinarySensorDeviceClass.PLUG,
        value="online",
    ),
    SpeedportBinarySensorEntityDescription(
        key="dualstack",
        name="Dual Stack",
        value="1",
    ),
    SpeedportBinarySensorEntityDescription(
        key="dsl_tunnel",
        name="DSL Tunnel",
        device_class=BinarySensorDeviceClass.CONNECTIVITY,
        condition_key="use_lte",
        value="1",
    ),
    SpeedportBinarySensorEntityDescription(
        key="lte_tunnel",
        name="LTE Tunnel",
        device_class=BinarySensorDeviceClass.CONNECTIVITY,
        condition_key="use_lte",
        value="1",
    ),
    SpeedportBinarySensorEntityDescription(
        key="hybrid_tunnel",
        name="Hybrid Tunnel",
        device_class=BinarySensorDeviceClass.CONNECTIVITY,
        condition_key="use_lte",
        value="1",
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
        if not description.condition_key
        or speedport.get(description.condition_key) == "1"
    ]

    async_add_entities(entities)


class SpeedportBinarySensor(SpeedportEntity, BinarySensorEntity):
    entity_description: SpeedportBinarySensorEntityDescription

    @property
    def is_on(self) -> bool | None:
        """Return true if the binary sensor is on."""
        return (
            self._speedport.get(self.entity_description.key)
            == self.entity_description.value
        )

    def available(self) -> bool:
        if self._speedport.get(self.entity_description.key) is None:
            return False
        return super().available
