"""Config flow for iHost integration."""
from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol

from homeassistant import config_entries, exceptions
from homeassistant.core import callback
from homeassistant.data_entry_flow import FlowResult
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
    DEFAULTS,
    DOMAIN,
)

_LOGGER = logging.getLogger(__name__)

def create_form(config_entry: config_entries.ConfigEntry = None):
    defaults = DEFAULTS
    if config_entry:
        defaults = config_entry.data
    fields = {
        vol.Required(CONF_PAIRING, default=defaults.get(CONF_PAIRING)): SelectSelector(
            SelectSelectorConfig(options=BUTTON1_MODES,
                                mode=SelectSelectorMode.DROPDOWN,
            )),
        vol.Optional(CONF_STATE, default=defaults.get(CONF_STATE)): BooleanSelector(),
        vol.Optional(CONF_BRIGHTNESS, default=defaults.get(CONF_BRIGHTNESS)): NumberSelector(
            NumberSelectorConfig(min=0, max=100, mode=NumberSelectorMode.SLIDER)
        ),
        vol.Optional(CONF_COLOR, default=defaults.get(CONF_COLOR)): ColorRGBSelector()
    }
    return fields

class ihostConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle ihost config flow."""

    VERSION = 2
    CONNECTION_CLASS = config_entries.CONN_CLASS_LOCAL_PUSH

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        await self.async_set_unique_id(DOMAIN)
        self._abort_if_unique_id_configured()

        if user_input is not None:
            return self.async_create_entry(title="iHost", data=user_input)
           
        return self.async_show_form(
            step_id="user", data_schema=vol.Schema(create_form())
        )

    @staticmethod
    @callback
    def async_get_options_flow(
        config_entry: config_entries.ConfigEntry,
    ) -> iHostOptionsFlowHandler:
        """Create the options flow."""
        return iHostOptionsFlowHandler(config_entry)

class iHostOptionsFlowHandler(config_entries.OptionsFlow):
    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        """Initialize options flow."""
        self.config_entry = config_entry

    async def async_step_init(self, user_input: None = None) -> FlowResult:
        """Manage the iHost options."""
        return await self.async_step_user()

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Manage the options."""
        current_config = self.config_entry.data
        if user_input is not None:
            self.hass.config_entries.async_update_entry(
                    self.config_entry,
                    data=user_input,
                    title=str("iHost"),
            )

            return self.async_create_entry(title="", data={})

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(create_form(self.config_entry))
        )
