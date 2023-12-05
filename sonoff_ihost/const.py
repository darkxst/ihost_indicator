DOMAIN = "sonoff_ihost"

PLATFORMS: list[str] = ["light","switch"]

BUTTON_LIST = ['power','pairing', 'security', 'music', 'reset']
BUTTON1_MODES = [
    {"value": "0", "label": "ZHA"},
    {"value": "1", "label": "Zigbee2MQTT"},
    {"value": "2", "label": "User"},
]

CONF_BRIGHTNESS = 'brightness'
CONF_COLOR = 'color'
CONF_PAIRING = "pairing"
CONF_STATE = 'state'

DEFAULTS = {
    CONF_BRIGHTNESS: 100,
    CONF_COLOR: [0, 0, 255],
    CONF_PAIRING: "0",
    CONF_STATE: True
}

PAIRING_MODES = ["ZHA", "Zigbee2MQTT", "User"]
EVENT_SPECIAL_BUTTON = "sonoff_ihost_button"

