"""YC1175 Hub"""
from __future__ import annotations

import asyncio
import logging

from yc1175_indicator import indicator
from homeassistant.core import HomeAssistant
from homeassistant.components import mqtt
from homeassistant.const import (
    EVENT_HOMEASSISTANT_START,
    EVENT_HOMEASSISTANT_STOP,
)
from .const import (
    BUTTON_LIST,
    EVENT_SPECIAL_BUTTON,
    PAIRING_MODES,
)

_LOGGER = logging.getLogger(__name__)

class Hub:
    """YC1175 Hub providing indicator control."""
    def __init__(self, hass: HomeAssistant, pair_mode: str) -> None:
        self.yc = indicator.HassAPI()
        self._pair_mode = int(pair_mode)
        self._hass = hass
        self._id = "ihost"
        self.indicator = []
        self.switches = []
        _LOGGER.info(f"Hub loaded: pairing mode: {PAIRING_MODES[self._pair_mode]}")

    @property
    def hub_id(self) -> str:
        """ID for hub."""
        return self._id
    
    #@callback test later need to add import  callback from core
    async def button_callback(self, idx, event):
        """Callback fired by button press in yc1175-library"""
        button_id = ord(idx)
        if button_id not in range(1,4):
            await self.async_fire_event(button_id)
        else:
            entity = next((s for s in self.switches if s.button_id==button_id), None)
            if entity is not None:
                await entity.async_toggle()

        _LOGGER.info(f"Button pressed: {idx}, type: {event}")

    async def async_fire_event(self, id):
        name = BUTTON_LIST[id]
        self._hass.bus.async_fire(f"{EVENT_SPECIAL_BUTTON}_{name}", {'button_id': id})
    
    async def enable_pairing(self, entity):
        delay = 180
        if self._pair_mode == 0:
            await self._hass.services.async_call('zha', 'permit', {'duration': delay})
        elif self._pair_mode == 1:
            payload = f'{{"value": true, "time": {delay}}}'
            await mqtt.async_publish(self._hass, "zigbee2mqtt/bridge/request/permit_join", payload)
        else:
            return

        await asyncio.sleep(delay)
        await entity.async_turn_off()

    async def handle_on_start(self, event):
        """ Turn on indicator on start"""
        await self.indicator[0].async_turn_on()
        self.yc.light_on(0)

    async def handle_on_stop(self, event):
        """Turn off all LEDS on stop"""
        for i in range(5):
            self.yc.light_off(i)

    async def handle_setup(self):
        await self.yc.setup()
        self._hass.bus.async_listen_once(EVENT_HOMEASSISTANT_START, self.handle_on_start)
        self._hass.bus.async_listen_once(EVENT_HOMEASSISTANT_STOP, self.handle_on_stop)
