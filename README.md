# Sonoff iHost Indicator
Home Assistant custom integration for controlling RGB indicator and buttons.

## Features
* Light entity for RGB indicator
* Set indicator on HA startup, turn of all LED's on shutdown
* Buttons for Pairing, Music and Security
* Pairing button can be set to activate pairing for ZHA or Zigbee2MQTT
* Reset and power buttons fire events
  * `sonoff_ihost_button_power`
  * `sonoff_ihost_button_reset`

## Installation
Install `sonoff_ihost` folder into:  
```~/config/custom_components/```  
Restart, then `Add integration` and find `iHost indicator`


## Known Issues
* Brightness on indicator not implemented yet
* Config dialog missing description texts
  

## Debug Logging
You can add the following to your `configuration.yaml` to get some debug logs:
```
logger:
  default: warning
  logs:
    custom_components.sonoff_ihost: debug
    yc1175_indicator.indicator: debug
```
## Support

If you would like to help support further development of my `HAOS for iHost` project consider buying me a coffee!

<a href="https://www.buymeacoffee.com/darkxst" target="_blank"><img src="img/blue-button.png" alt="Buy Me A Coffee" height="41" width="174"></a>


