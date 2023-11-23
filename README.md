# Sonoff iHost Indicator
Home Assistant custom integration for controlling RGB indicator and buttons.

## Features
* Light entity for RGB indicator
* Buttons for Pairing, Music and Security

## Installation
Install into
```~/config/custom_components/```
Restart, then `Add integration` and find `iHost indicator`


## Known Issues
* Brightness on indicator not implemented yet
* Config dialog missing description texts
  

## Debug Logging
You can add the following to your `configuration.yaml` to get some debug logs
```
logger:
  default: warning
  logs:
    custom_components.sonoff_ihost: debug
    yc1175_indicator.indicator: debug
```
