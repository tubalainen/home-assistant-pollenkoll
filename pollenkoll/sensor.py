"""
Support for getting current pollen levels from Pollenkollen.se
Visit https://pollenkoll.se/pollenprognos/ to find available cities
Visit https://pollenkoll.se/pollenprognos-ostersund/ to find available allergens

Example configuration

sensor:
  - platform: pollenkoll
    sensors:
      - city: Borlänge
        hide_city_in_frontend: True
        allergens:
          - Al
          - Alm
          - Hassel
      - city: Jönköping
        hide_city_in_frontend: False
        allergens:
          - Al
          - Alm
          - Hassel
      - city: Skövde
        allergens:
          - Al
          - Alm
          - Hassel
"""

import logging
import json

from collections import namedtuple
from datetime import timedelta

import voluptuous as vol

import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.entity import Entity
from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.components.sensor.rest import RestData
from homeassistant.const import (CONF_NAME)

_LOGGER = logging.getLogger(__name__)
_ENDPOINT = 'https://pollenkoll.se/wp-content/themes/pollenkoll/api/get_all.json'

ATTR_POLLEN = 'pollen'
ATTR_TODAY = 'day0_value'
ATTR_TYPE = 'type'

DEFAULT_NAME = 'Pollenkoll'
DEFAULT_VERIFY_SSL = True
CONF_SENSORS = 'sensors'

SCAN_INTERVAL = timedelta(hours=12)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
    vol.Required(CONF_SENSORS, default=[]): cv.ensure_list,
})


def setup_platform(hass, config, add_devices, discovery_info=None):
    """Set up the PVOutput sensor."""
    name = config.get(CONF_NAME)
    sensors = config.get('sensors')
    method = 'GET'
    payload = ''
    auth = ''
    verify_ssl = DEFAULT_VERIFY_SSL
    headers = {}

    rest = RestData(method, _ENDPOINT, auth, headers, payload, verify_ssl)
    rest.update()

    if rest.data is None:
        _LOGGER.error("Unable to fetch data from Pollenkollen")
        return False

    for sensor in sensors:
        for allergen in sensor['allergens']:
            add_devices([PollenkollSensor(rest, name, sensor, allergen)], True)

# pylint: disable=no-member
class PollenkollSensor(Entity):
    """Representation of a PVOutput sensor."""

    def __init__(self, rest, name, sensor, allergen):
        """Initialize a PVOutput sensor."""
        self._rest = rest
        self._item = sensor
        self._city = sensor['city']
        self._state = None
        if 'hide_city_in_frontend' in sensor:
            if sensor['hide_city_in_frontend']:
                self._name = "Pollennivå " + allergen
            else:
                self._name = "Pollennivå " + sensor['city'] + " " + allergen
        else:
            self._name = "Pollennivå " + sensor['city'] + " " + allergen
        self._allergen = allergen
        self._pollen = None
        self._result = None
        self._status = namedtuple(
            'status', [ATTR_POLLEN, ATTR_TODAY, ATTR_TYPE])

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def state(self):
        """Return the state of the device."""
        if self._state is not None:
            return self._state
        return None

    @property
    def device_state_attributes(self):
        """Return the state attributes of the monitored installation."""
        if self._pollen is not None:
            return self._pollen

    def update(self):
        """Get the latest data from the PVOutput API and updates the state."""
        try:
            pollen = {}
            self._rest.update()
            self._result = json.loads(self._rest.data)

            for datapart in self._result:
                CitiesData = datapart['CitiesData'];

            for jsonitem in CitiesData:
                if jsonitem['name'] in self._city:
                    pollen = jsonitem['pollen'];

            self._pollen = {}

            for allergen in pollen:
                if allergen['type'] == self._allergen:
                    self._state = allergen['day0_value']
                #self._pollen.update({allergen['type']: allergen['day0_value']})

        except TypeError as e:
            self._result = None
            _LOGGER.error(
                "Unable to fetch data from Pollenkoll. " + str(e))
