# Speedport Integration for Home Assistant

[![hacs_badge](https://img.shields.io/badge/hacs-Default-41BDF5.svg)](https://hacs.xyz)
[![GitHub](https://img.shields.io/github/license/Andre0512/speedport?color=red)](https://github.com/Andre0512/speedport/blob/main/LICENSE)
[![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/Andre0512/speedport/python_check.yml?branch=main&label=checks)](https://github.com/Andre0512/speedport/actions/workflows/python_check.yml)
[![Buy Me a Coffee](https://img.shields.io/badge/Buy%20Me%20a%20Coffee-donate-orange.svg)](https://www.buymeacoffee.com/andre0512)  
[![GitHub release (latest by date)](https://img.shields.io/github/v/release/Andre0512/speedport?color=green)](https://github.com/Andre0512/speedport/releases/latest)
[![GitHub all releases](https://img.shields.io/github/downloads/Andre0512/speedport/latest/total?color=blue&label=downloads)](https://tooomm.github.io/github-release-stats/?username=Andre0512&repository=speedport)
[![GitHub all releases](https://img.shields.io/github/downloads/Andre0512/speedport/total?color=blue&label=total%20downloads)](https://tooomm.github.io/github-release-stats/?username=Andre0512&repository=speedport)  

Telekom Speedport Integration for Home Assistant based
on [speedport-api](https://github.com/Andre0512/speedport-api.git).

## Features

- Track presence of connected devices
- Turn on/off wifi (guest/office/normal)
- Reconnect, reboot, wps on
- Sensors (IP-Addresses, Upload/Download, Connection, ...)

## Supported devices

* Speedport Smart 3
* Speedport Smart 4

## Installation
**Method 1:** [![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=Andre0512&repository=speedport&category=integration)

**Method 2:** [HACS](https://hacs.xyz/) > Integrations > Add Integration > **Speedport** > Install  

**Method 3:** Manually copy `speedport` folder from [latest release](https://github.com/Andre0512/speedport/releases/latest) to `config/custom_components` folder.

_Restart Home Assistant_

## Configuration

**Method 1**: [![Open your Home Assistant instance and start setting up a new integration.](https://my.home-assistant.io/badges/config_flow_start.svg)](https://my.home-assistant.io/redirect/config_flow_start/?domain=speedport)

**Method 2**: Settings > Devices & Services > Add Integration > **Speedport**  
_If the integration is not in the list, you need to clear the browser cache._

### Further Information

If you have email notifications enabled, make sure you have the "A security related event has occurred" option unchecked
or you will receive a lot of emails, see [#1](https://github.com/Andre0512/speedport/issues/1).

## Support

If you find this project helpful and would like to support its development, you can buy me a coffee! ☕

[!["Buy Me A Coffee"](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/andre0512)

Don't forget to star the repository if you found it useful! ⭐
