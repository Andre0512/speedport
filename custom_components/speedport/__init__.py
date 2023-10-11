"""The Speedport integration."""

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers import aiohttp_client
from speedport import Speedport

from .const import DOMAIN

PLATFORMS: list[Platform] = [Platform.BUTTON, Platform.DEVICE_TRACKER, Platform.SWITCH]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Speedport from a config entry."""
    session = aiohttp_client.async_get_clientsession(hass)

    hass.data.setdefault(DOMAIN, {})
    speedport = await Speedport(
        host=entry.data["host"], password=entry.data["password"], session=session
    ).create()
    hass.data[DOMAIN][entry.entry_id] = speedport

    for platform in PLATFORMS:
        hass.async_create_task(
            hass.config_entries.async_forward_entry_setup(entry, platform)
        )
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        speedport = hass.data[DOMAIN].pop(entry.entry_id)
        await speedport.close()

    return unload_ok
