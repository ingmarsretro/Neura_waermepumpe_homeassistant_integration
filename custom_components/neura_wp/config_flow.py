"""Config flow for the Neura heat pump."""

from __future__ import annotations

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_HOST, CONF_PASSWORD, CONF_PORT, CONF_USERNAME
from homeassistant.helpers.selector import NumberSelector, NumberSelectorConfig, NumberSelectorMode, TextSelector, TextSelectorConfig, TextSelectorType

from .client import NeuraClient, NeuraError
from .const import CONF_SALT, DEFAULT_HOST, DEFAULT_PORT, DOMAIN

DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_HOST, default=DEFAULT_HOST): str,
        vol.Required(CONF_PORT, default=DEFAULT_PORT): NumberSelector(
            NumberSelectorConfig(min=1, max=65535, mode=NumberSelectorMode.BOX, step=1)
        ),
        vol.Optional(CONF_USERNAME, default=""): str,
        vol.Optional(CONF_PASSWORD, default=""): TextSelector(
            TextSelectorConfig(type=TextSelectorType.PASSWORD)
        ),
        vol.Optional(CONF_SALT, default=""): str,
    }
)


def _probe(user_input: dict) -> None:
    client = NeuraClient(
        user_input[CONF_HOST],
        int(user_input[CONF_PORT]),
        user_input.get(CONF_USERNAME, ""),
        user_input.get(CONF_PASSWORD, ""),
        user_input.get(CONF_SALT, ""),
    )
    try:
        client.connect()
    finally:
        client.disconnect()


class NeuraConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Set up a connection to the controller on the local network."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors = {}
        if user_input is not None:
            user_input[CONF_PORT] = int(user_input[CONF_PORT])
            await self.async_set_unique_id(user_input[CONF_HOST])
            self._abort_if_unique_id_configured()
            try:
                await self.hass.async_add_executor_job(_probe, user_input)
            except NeuraError:
                errors["base"] = "cannot_connect"
            except OSError:
                errors["base"] = "cannot_connect"
            else:
                return self.async_create_entry(title=f"Neura {user_input[CONF_HOST]}", data=user_input)
        return self.async_show_form(step_id="user", data_schema=DATA_SCHEMA, errors=errors)
