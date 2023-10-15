# Speedport Integration
[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg)](https://hacs.xyz)
[![GitHub](https://img.shields.io/github/license/Andre0512/speedport?color=red)](https://github.com/Andre0512/speedport/blob/main/LICENSE)
[![GitHub release (latest by date)](https://img.shields.io/github/v/release/Andre0512/speedport?color=green)](https://github.com/Andre0512/speedport/releases/latest)
[![GitHub all releases](https://img.shields.io/github/downloads/Andre0512/speedport/total?color=blue&label=total%20downloads)](https://tooomm.github.io/github-release-stats/?username=Andre0512&repository=speedport)

Telekom Speedport Integration for Home Assistant based on [speedport-api](https://github.com/Andre0512/speedport-api.git)

- Track presence of connected devices
- Turn on/off wifi (guest/office/normal)
- Reconnect, reboot, wps on
- Sensors (IP-Addresses, Upload/Download, Connection, ...)

## Installation
#### Installing via HACS
1. You need to have installed [HACS](https://hacs.xyz/)
2. Go to HACS -> Integrations
3. Add this repo (`https://github.com/Andre0512/speedport.git`) into your HACS custom repositories
4. Search for Speedport and download it
5. Restart your Home Assistant
6. Go to Settings -> Devices & Services
7. Shift reload your browser
8. Click Add Integration
9. Search for Speedport 
10. Insert your router IP/hostname and your password

## Configuration

**Method 1**: [![Open your Home Assistant instance and start setting up a new integration.](https://my.home-assistant.io/badges/config_flow_start.svg)](https://my.home-assistant.io/redirect/config_flow_start/?domain=speedport)

**Method 2**: Settings > Devices & Services > Add Integration > **Speedport**  
_If the integration is not in the list, you need to clear the browser cache._


## Working devices
* Speedport Smart 4

So far I can only confirm that it works with my router 🙂

## Support
If you find this project helpful and would like to support its development, you can buy me a coffee! ☕

[!["Buy Me A Coffee"](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/andre0512)

Don't forget to star the repository if you found it useful! ⭐
