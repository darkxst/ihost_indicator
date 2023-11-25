"""Platform for yc1175 RGB indicator."""
from __future__ import annotations

import asyncio
import colorsys
import logging

from .const import DOMAIN
from yc1175_indicator import indicator
import voluptuous as vol

import homeassistant.helpers.config_validation as cv
from homeassistant.components.light import (
    ATTR_BRIGHTNESS,
    ATTR_EFFECT,
    ATTR_RGB_COLOR,                                     
    ColorMode,
    LightEntity,
    LightEntityFeature,
)
from homeassistant.const import CONF_NAME, EVENT_HOMEASSISTANT_START
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Setup indicator entity."""
    hub = hass.data[DOMAIN][entry.entry_id]
    hub.indicator.append(iHostLight(hub))
    async_add_entities(hub.indicator)

class iHostLight(LightEntity):
    """Representation for the iHost RGB indicator."""

    def __init__(self, hub) -> None:
        """Initialise indicator."""
        self._idx = 4
        self._hub = hub
        self._name = "indicator"
        self._brightness = hub.defaults("brightness")
        self._effect = "on"
        self._rgb_color = hub.defaults("color")
        self._state = not hub.defaults("state")
        self._color_mode = ColorMode.RGB
        self._attr_unique_id = f"{DOMAIN}_{self._name}"
        self._attr_should_poll = False
        self._attr_supported_color_modes = {self.color_mode}
        self._attr_supported_features |= LightEntityFeature.EFFECT
    
    @property
    def brightness(self) -> int | None:
        """Return the brightness of this light. """
        return self._brightness
    
    @property
    def color_mode(self) -> str | None:
        """Return the color mode of the light."""
        return ColorMode.RGB

    @property
    def effect_list(self):
        effect_list = self._hub.yc.effect_list()
        return effect_list[1:]

    @property
    def effect(self):
        """Return the current effect of this light."""
        return self._effect

    @property
    def name(self) -> str:
        """Return the display name of this light."""
        return self._name

    @property
    def is_on(self) -> bool | None:
        """Return true if light is on."""
        return self._state
    
    @property
    def rgb_color(self) -> tuple[int, int, int]:
        """Return the rgb color value [int, int, int]."""
        return self._rgb_color

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Set inicator light to turn off."""

        self._brightness = kwargs.get(ATTR_BRIGHTNESS, 255)

        if ATTR_EFFECT in kwargs:
            self._effect = kwargs[ATTR_EFFECT]

        if ATTR_RGB_COLOR in kwargs:
            self._rgb_color = kwargs[ATTR_RGB_COLOR]

        if self._effect:
            effect_idx = self._hub.yc.effect_list().index(self._effect)

        rgb = self._rgb_color
        if self._brightness < 255:
            rgb = self.scale_rgb(rgb, self._brightness)
        
        _LOGGER.debug(f"rgb data {self._rgb_color}, {rgb}, {self._brightness}, {self._effect}")

        self._hub.yc.light_on(self._idx, effect_idx, rgb)
        
        self._state = True
        if effect_idx == 6:
            await asyncio.sleep(1)
            self._state = False
        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Set inicator light to turn off."""
        _LOGGER.info("turn off indicator")
        self._state = False
        self.async_write_ha_state()

        self._hub.yc.light_off(self._idx)

    def scale_rgb(self, rgb, brightness):
        """Scale rgb values based on brightness"""
        rgb = tuple(x/255.0 for x in rgb)
        h, s, v = colorsys.rgb_to_hsv(*rgb)

        # Scale brightness
        v *= brightness / 255.0

        rgb_scaled = tuple(int(x*255) for x in colorsys.hsv_to_rgb(h, s, v))
        return rgb_scaled