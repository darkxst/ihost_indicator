"""
Switch platform for Sonoff iHost.

There are three buttons (as labeled on the ihost)
1. Pairing
2. Security
3. Music
Power and Reset not implemented here.

"""
from __future__ import annotations

import asyncio
import logging

from .const import BUTTON_LIST, DOMAIN
from homeassistant.components.switch import SwitchDeviceClass, SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    
    hub = hass.data[DOMAIN][entry.entry_id]
    switches = []

    for button_id in range(1, 4):
        switch = iHostSwitch(hass, button_id, hub)
        hub.switches.append(switch)
        switches.append(switch)

    async_add_entities(switches)

class iHostSwitch(SwitchEntity):
    """Switch based on a button press from my device."""
    _attr_device_class = SwitchDeviceClass.SWITCH

    def __init__(self, hass, button_id, hub): 
        self._button_id = button_id
        self._attr_name = BUTTON_LIST[button_id]
        self._attr_should_poll = False
        self._attr_unique_id = f"{DOMAIN}_button_{button_id}"
        self._hass = hass
        self._hub = hub
        self._state = False

    @property
    def is_on(self):
        """Return whether switch is on."""
        return self._state
    
    @property
    def button_id(self):
        """Return button id."""
        return self._button_id

    async def async_turn_on(self, **kwargs):
        """Turn the switch on."""
        self._state = True
        self.async_write_ha_state()
        self._hub.yc.light_on(self._button_id)
        if self._button_id == 1:
            self._hass.async_create_task(self._hub.enable_pairing(entity=self))
        _LOGGER.info(f"Button {self._button_id} is on: {self.is_on}")

    async def async_turn_off(self, **kwargs):
        """Turn the switch off."""
        self._state = False
        self.async_write_ha_state()
        self._hub.yc.light_off(self._button_id)
        _LOGGER.info(f"Button  {self._button_id} is on: {self.is_on}")
