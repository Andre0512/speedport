from datetime import datetime

import pytz
from homeassistant.components.sensor import (
    SensorEntityDescription,
    SensorDeviceClass,
    SensorStateClass,
    SensorEntity,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    EntityCategory,
    UnitOfDataRate,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import StateType
from speedport import Speedport

from custom_components.speedport import DOMAIN
from custom_components.speedport.device import SpeedportEntity

SENSORS: tuple[SensorEntityDescription, ...] = (
    SensorEntityDescription(
        key="public_ip_v4",
        name="IPv4",
        icon="mdi:earth",
    ),
    SensorEntityDescription(
        key="public_ip_v6",
        name="IPv6",
        icon="mdi:earth",
    ),
    SensorEntityDescription(
        key="inet_uptime",
        name="Internet Uptime",
        device_class=SensorDeviceClass.TIMESTAMP,
    ),
    SensorEntityDescription(
        key="inet_upload",
        name="Upload",
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfDataRate.KILOBITS_PER_SECOND,
        device_class=SensorDeviceClass.DATA_RATE,
        icon="mdi:upload",
    ),
    SensorEntityDescription(
        key="inet_download",
        name="Download",
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfDataRate.KILOBITS_PER_SECOND,
        device_class=SensorDeviceClass.DATA_RATE,
        icon="mdi:download",
    ),
    SensorEntityDescription(
        key="dsl_upstream",
        name="DSL-Link Upstream",
        native_unit_of_measurement=UnitOfDataRate.KILOBITS_PER_SECOND,
        device_class=SensorDeviceClass.DATA_RATE,
        icon="mdi:upload",
    ),
    SensorEntityDescription(
        key="dsl_downstream",
        name="DSL-Link Downstream",
        native_unit_of_measurement=UnitOfDataRate.KILOBITS_PER_SECOND,
        device_class=SensorDeviceClass.DATA_RATE,
        icon="mdi:download",
    ),
)


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Set up entry."""
    speedport: Speedport = hass.data[DOMAIN][entry.entry_id]

    entities = [
        SpeedportBinarySensor(hass, speedport, description) for description in SENSORS
    ]

    async_add_entities(entities)


class SpeedportBinarySensor(SpeedportEntity, SensorEntity):
    entity_description: SensorEntityDescription

    @property
    def native_value(self) -> StateType:
        """Return the value reported by the sensor."""
        if (data := self._speedport.get(self.entity_description.key)) is None:
            return None
        if self.entity_description.device_class == SensorDeviceClass.TIMESTAMP:
            date = datetime.strptime(data, "%Y-%m-%d %H:%M:%S")
            return pytz.timezone("Europe/Berlin").localize(date)
        return data

    def available(self) -> bool:
        if self._speedport.get(self.entity_description.key) is None:
            return False
        return super().available
