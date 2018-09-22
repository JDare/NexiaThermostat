import requests
from bs4 import BeautifulSoup

import time


class NexiaThermostat:

    ROOT_URL = "https://www.mynexia.com"
    AUTH_FAILED_STRING = "https://www.mynexia.com/login"

    username = None
    password = None
    house_id = None

    session = None
    last_csrf = None

    thermostat_json = None

    def __init__(self, house_id, username=None, password=None, auto_login=True):

        self.username = username
        self.password = password
        self.house_id = house_id

        if auto_login:
            self.login()

        self.session = requests.session()
        self.session.max_redirects = 3

    def login(self):
        print("Logging in as " + self.username)
        token = self.get_authenticity_token("/login")
        if token:
            payload = {
                'login': self.username,
                'password': self.password,
                token['param']: token['token']
            }
            self.last_csrf = token['token']
            print("posting login")
            r = self.post_url("/session", payload)
            if r.status_code == 200:
                return True

            print("Failed to login", r.text)
            return False
        else:
            print("Failed to get csrf token")
        return False

    def get_authenticity_token(self, url):
        print("getting auth token")
        r = self.get_url(url)
        if r.status_code == 200:
            print("parsing csrf token")
            soup = BeautifulSoup(r.text, 'html5lib')
            param = soup.find("meta", attrs={'name': "csrf-param"})
            token = soup.find("meta", attrs={'name': "csrf-token"})
            if token and param:
                return {
                    "token": token['content'],
                    "param": param['content']
                }
        return False

    def put_url(self, url, payload):
        print("Starting PUT Request")
        request_url = self.ROOT_URL + url

        if not self.last_csrf:
            self.login()

        headers = {
            "X-CSRF-Token": self.last_csrf,
            "X-Requested-With": "XMLHttpRequest"
        }
        print(headers, payload)
        try:
            r = self.session.put(request_url, payload, headers=headers, allow_redirects=False)
        except requests.RequestException as e:
            print("Error putting url", str(e))
            return None
        if r.status_code == 302 and self.AUTH_FAILED_STRING in r.text:
            # assuming its redirecting to login
            time.sleep(1)
            if not self.login():
                return False
            time.sleep(1)
            return self.put_url(url, payload)

        if r.status_code == 200:
            return r
        return False

    def post_url(self, url, payload):
        request_url = self.ROOT_URL + url
        try:
            r = self.session.post(request_url, payload)
        except requests.RequestException as e:
            print("Error posting url", str(e))
            return None

        if r.status_code == 302 and self.AUTH_FAILED_STRING in r.text:
            # assuming its redirecting to login
            if not self.login():
                return False
            return self.post_url(url, payload)

        if r.status_code == 200:
            return r
        return False

    def get_url(self, url):
        request_url = self.ROOT_URL + url

        try:
            r = self.session.get(request_url, allow_redirects=False)
        except requests.RequestException as e:
            print("Error getting url", str(e))
            return None

        if r.status_code == 302 and self.AUTH_FAILED_STRING in r.text:
            # assuming its redirecting to login
            if not self.login():
                return False
            return self.get_url(url)

        if r.status_code == 200:
            return r
        return False

    def get_zone_key(self, key, zone=0):
        zone = self.get_zone(zone)
        if not zone:
            return False

        if key in zone:
            return zone[key]

        return False

    def get_thermostat_key(self, key):
        thermostat = self.get_thermostat_json()
        if thermostat and key in thermostat:
            return thermostat[key]
        return False

    def get_zone(self, zone=0):
        thermostat = self.get_thermostat_json()
        if not thermostat:
            return None
        if len(thermostat['zones']) > zone:
            return thermostat['zones'][zone]
        return None

    def get_thermostat_json(self):
        if not self.thermostat_json:
            r = self.get_url("/houses/" + str(self.house_id) + "/xxl_thermostats")
            if r and r.status_code == 200:
                ts = r.json()
                if 0 in ts:
                    self.thermostat_json = ts[0]
            else:
                print("Failed to get thermostat JSON, session probably timed out")
                print(r.status_code, r.headers)
                return None
        return self.thermostat_json

    def get_zone_cooling_setpoint(self, zone=0):
        return self.get_zone_key('cooling_setpoint', zone=zone)

    def get_zone_heating_setpoint(self, zone=0):
        return self.get_zone_key('heating_setpoint', zone=zone)

    def get_zone_temperature(self, zone=0):
        return self.get_zone_key('temperature', zone=zone)

    def get_fan_mode(self):
        return self.get_thermostat_key('fan_mode')

    def get_outdoor_temperature(self):
        return self.get_thermostat_key('outdoor_temperature')

    def get_setpoint_url(self, zone=0):
        zone_id = self.get_zone_key('id', zone)
        return "/houses/" + str(self.house_id) + "/xxl_zones/" + str(zone_id) + "/setpoints"

    def set_min_max_temp(self, min_temperature, max_temperature, zone=0):
        url = self.get_setpoint_url(zone)

        data = {
            'cooling_setpoint': max_temperature,
            'cooling_integer': max_temperature,
            'heating_setpoint': min_temperature,
            'heating_integer': min_temperature
        }

        r = self.put_url(url, data)

        if r.status_code == 200:
            return True
        return False

