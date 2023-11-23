DOMAIN = "sonoff_ihost"

PLATFORMS: list[str] = ["light","switch"]

BUTTON_LIST = ['power','pairing', 'security', 'music', 'reset']
CONF_PAIRING = "pairing"
DEFAULT_PAIRING = "0"
BUTTON1_MODES = [
    {"value": "0", "label": "ZHA"},
    {"value": "1", "label": "Zigbee2MQTT"},
    {"value": "2", "label": "User"},            
]
PAIRING_MODES = ["ZHA", "Zigbee2MQTT", "User"]
EVENT_SPECIAL_BUTTON = "sonoff_ihost_button"

