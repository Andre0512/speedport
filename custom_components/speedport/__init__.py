"""The Speedport integration."""

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from speedport import Speedport

from .const import DOMAIN

PLATFORMS: list[Platform] = [Platform.BUTTON, Platform.DEVICE_TRACKER, Platform.SWITCH]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Speedport from a config entry."""

    hass.data.setdefault(DOMAIN, {})
    speedport = Speedport(entry.data["host"])
    await speedport.login(entry.data["password"])
    hass.data[DOMAIN][entry.entry_id] = speedport

    for platform in PLATFORMS:
        hass.async_create_task(
            hass.config_entries.async_forward_entry_setup(entry, platform)
        )
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok
