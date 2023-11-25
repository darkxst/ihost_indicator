"""YC1175 Hub"""
from __future__ import annotations

import asyncio
import logging
from typing import Any

from yc1175_indicator import indicator
from homeassistant.core import Event, HomeAssistant
from homeassistant.components import mqtt
from homeassistant.components.switch import SwitchEntity
from homeassistant.const import (
    EVENT_HOMEASSISTANT_START,
    EVENT_HOMEASSISTANT_STOP,
)

from .const import (
    CONF_BRIGHTNESS,
    CONF_COLOR,
    CONF_PAIRING,
    CONF_STATE,
    EVENT_SPECIAL_BUTTON,
    PAIRING_MODES,
)

_LOGGER = logging.getLogger(__name__)

class Hub:
    """YC1175 Hub providing indicator control."""
    def __init__(self, hass: HomeAssistant, entry_data: dict[str, Any]) -> None:
        self.yc = indicator.HassAPI()
        self.BUTTON_LIST = self.yc.button_list()
        self._pair_mode = int(entry_data[CONF_PAIRING])
        self._defaults = {
            CONF_BRIGHTNESS: int(entry_data[CONF_BRIGHTNESS] * 2.55),
            CONF_COLOR: tuple(entry_data[CONF_COLOR]),
            CONF_STATE: entry_data[CONF_STATE]
        }

        self._hass = hass
        self._id = "ihost"
        self.indicator = []
        self.switches = []
        _LOGGER.info(f"Hub loaded: pairing mode: {PAIRING_MODES[self._pair_mode]}")

    @property
    def hub_id(self) -> str:
        """ID for hub."""
        return self._id

    def defaults(self, key:str):
        """Default properties by key"""
        return self._defaults[key]

    #@callback test later need to add import  callback from core
    async def button_callback(self, idx:bytes, event:bytes) -> None:
        """Callback fired by button press in yc1175-library"""
        button_id = ord(idx)
        if button_id not in range(1,4):
            await self.async_fire_event(button_id)
        else:
            entity = next((s for s in self.switches if s.button_id==button_id), None)
            if entity is not None:
                await entity.async_toggle()

        _LOGGER.info(f"Button pressed: {idx}, type: {event}")

    async def async_fire_event(self, id:int) -> None:
        name = self.BUTTON_LIST[id]
        self._hass.bus.async_fire(f"{EVENT_SPECIAL_BUTTON}_{name}", {'button_id': id})
    
    async def enable_pairing(self, entity:SwitchEntity) -> None:
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

    async def handle_on_start(self, event:Event) -> None:
        """ Turn on indicator on start"""
        await self.indicator[0].async_toggle()
        self.yc.light_on(0)

    async def handle_on_stop(self, event:Event) -> None:
        """Turn off all LEDS on stop"""
        for i in range(5):
            self.yc.light_off(i)

    async def handle_setup(self) -> None:
        await self.yc.setup()
        self._hass.bus.async_listen_once(EVENT_HOMEASSISTANT_START, self.handle_on_start)
        self._hass.bus.async_listen_once(EVENT_HOMEASSISTANT_STOP, self.handle_on_stop)
