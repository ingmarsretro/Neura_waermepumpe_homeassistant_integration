"""Neura ground-source heat pump."""

from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_HOST, CONF_PASSWORD, CONF_PORT, CONF_USERNAME
from homeassistant.core import HomeAssistant

from .client import NeuraClient
from .const import CONF_SALT, DOMAIN, PLATFORMS
from .coordinator import NeuraCoordinator
from .views import async_register_panel, async_setup_http, async_unregister_panel


async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    hass.data.setdefault(DOMAIN, {})
    async_setup_http(hass)
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    hass.data.setdefault(DOMAIN, {})
    async_setup_http(hass)
    client = NeuraClient(
        entry.data[CONF_HOST],
        entry.data.get(CONF_PORT, 80),
        entry.data.get(CONF_USERNAME, ""),
        entry.data.get(CONF_PASSWORD, ""),
        entry.data.get(CONF_SALT, ""),
    )
    coordinator = NeuraCoordinator(hass, client)
    await coordinator.async_config_entry_first_refresh()
    hass.data[DOMAIN][entry.entry_id] = coordinator
    async_register_panel(hass)
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if not unload_ok:
        return False
    coordinator = hass.data[DOMAIN].pop(entry.entry_id, None)
    if coordinator is not None:
        await hass.async_add_executor_job(coordinator.client.disconnect)
    async_unregister_panel(hass)
    return True
