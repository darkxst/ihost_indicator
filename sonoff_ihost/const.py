DOMAIN = "sonoff_ihost"

PLATFORMS: list[str] = ["light","switch"]

BUTTON_LIST = ['power','pairing', 'security', 'music', 'reset']

CONF_BRIGHTNESS = 'brightness'
CONF_COLOR = 'color'
CONF_PAIRING = "pairing"
CONF_STATE = 'state'

DEFAULT_BRIGHTNESS = 100
DEFAULT_COLOR = [0, 0, 255]
DEFAULT_PAIRING = "0"
DEFAULT_STATE = True

BUTTON1_MODES = [
    {"value": "0", "label": "ZHA"},
    {"value": "1", "label": "Zigbee2MQTT"},
    {"value": "2", "label": "User"},            
]
PAIRING_MODES = ["ZHA", "Zigbee2MQTT", "User"]
EVENT_SPECIAL_BUTTON = "sonoff_ihost_button"

