"""Config flow for iHost integration."""
from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol

from homeassistant import config_entries, exceptions
from homeassistant.core import HomeAssistant
from homeassistant.helpers.selector import (
    BooleanSelector,
    ColorRGBSelector,
    NumberSelector,
    NumberSelectorConfig,
    NumberSelectorMode,
    SelectSelector,
    SelectSelectorConfig,
    SelectSelectorMode,
)

from .const import (
    BUTTON1_MODES,
    CONF_BRIGHTNESS,
    CONF_COLOR,
    CONF_PAIRING,
    CONF_STATE,
    DEFAULT_BRIGHTNESS,
    DEFAULT_COLOR,
    DEFAULT_PAIRING,
    DEFAULT_STATE,
    DOMAIN,
)

DATA_SCHEMA = vol.Schema({
    vol.Required(CONF_PAIRING, default=DEFAULT_PAIRING): SelectSelector(
        SelectSelectorConfig(options=BUTTON1_MODES,
                             mode=SelectSelectorMode.DROPDOWN,
        )),
    vol.Optional(CONF_STATE, default=DEFAULT_STATE): BooleanSelector(),
    vol.Optional(CONF_BRIGHTNESS, default=DEFAULT_BRIGHTNESS): NumberSelector(
        NumberSelectorConfig(min=0, max=100, mode=NumberSelectorMode.SLIDER)
    ),
    vol.Optional(CONF_COLOR, default=DEFAULT_COLOR): ColorRGBSelector()
})

class ihostConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle ihost config flow."""

    VERSION = 2
    CONNECTION_CLASS = config_entries.CONN_CLASS_LOCAL_PUSH

    async def async_step_user(self, user_input=None):
        await self.async_set_unique_id(DOMAIN)
        self._abort_if_unique_id_configured()

        if user_input is not None:
            return self.async_create_entry(title="iHost", data=user_input)
           
        return self.async_show_form(
            step_id="user", data_schema=DATA_SCHEMA
        )