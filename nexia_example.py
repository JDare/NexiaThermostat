from nexia_thermostat import NexiaThermostat

NEXIA_USERNAME = ""
NEXIA_PASSWORD = ""
HOUSE_ID = ""


def main():
    print("Starting Example ...")
    nexia_instance = NexiaThermostat(username=NEXIA_USERNAME, password=NEXIA_PASSWORD, house_id=HOUSE_ID, auto_login=False)
    print(nexia_instance.get_zone_temperature())
    nexia_instance.set_min_max_temp(70, 85)


if __name__ == '__main__':
    main()

