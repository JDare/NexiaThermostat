# Nexia/Trane Thermostat Library

This library utilizes the Nexia web portal to simulate requests for getting and setting data for your thermostat. It has only been tested with an _American Standard Acculink Platinum 850 WiFi Thermostat_ but it should work with any _XXL_ thermostats which use the Nexia Web Portal (potentially including various Trane thermostats, as the Nexia registers as a _TraneXl850_).

Please note as this is not using any official API, Nexia may update their services at anytime causing this library to stop working. You are using this at your own risk and should not rely on this in any production capacity.

## Usage

`nexia_instance = NexiaThermostat(username=NEXIA_USERNAME, password=NEXIA_PASSWORD, house_id=HOUSE_ID)`

Note, using this library requires your _house_id_, this can be found by logging into your nexia portal (mynexia.com) and viewing the source code of the page. Around Line 54 you should see some javascript similar to `window.Nexia.modes.houseId = 12345;`. This number is your house_id.

To get temperature `nexia_instance.get_zone_temperature()`

To set min/max temperatures `nexia_instance.set_min_max_temp(68, 80)`