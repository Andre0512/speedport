"""The Speedport integration."""
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers import aiohttp_client
from speedport import Speedport

from .config_flow import OptionsFlowHandler
from .const import DOMAIN

PLATFORMS: list[Platform] = [
    Platform.BUTTON,
    Platform.DEVICE_TRACKER,
    Platform.SWITCH,
    Platform.BINARY_SENSOR,
    Platform.SENSOR,
]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Speedport from a config entry."""

    hass.data.setdefault(DOMAIN, {})
    speedport = await Speedport(
        host=entry.data["host"],
        password=entry.data["password"],
        session=aiohttp_client.async_get_clientsession(hass),
        pause_time=entry.options.get("pause_time", 5),
    ).create()
    hass.data[DOMAIN][entry.entry_id] = speedport
    hass.data[DOMAIN]["coordinators"] = {}

    entry.async_on_unload(entry.add_update_listener(update_listener))

    for platform in PLATFORMS:
        hass.async_create_task(
            hass.config_entries.async_forward_entry_setup(entry, platform)
        )
    return True


async def update_listener(hass, entry):
    """Handle options update."""
    speedport: Speedport = hass.data[DOMAIN][entry.entry_id]
    speedport.set_pause_time(entry.options.get("pause_time", 5))


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        speedport = hass.data[DOMAIN].pop(entry.entry_id)
        await speedport.close()

    return unload_ok
