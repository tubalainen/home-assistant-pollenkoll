"""
Support for getting current pollen levels from Pollenkollen.se
Visit https://pollenkoll.se/pollenprognos/ to find available cities
Visit https://pollenkoll.se/pollenprognos-ostersund/ to find available allergens

Example configuration

sensor:
  - platform: pollenkoll
    sensors:
      - city: Forshaga
        hide_city_in_frontend: True # (OPTIONAL)
        days_to_track: 2 #(OPTIONAL, possible values 0-3, 0 = today, 1 = today and tomorrow, 2 = today tomorrow and day after tomorrow and so on )
        allergens:
          - Al
          - Alm
          - Hassel
      - city: Jönköping
        hide_city_in_frontend: False #(OPTIONAL)
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
from homeassistant.components.rest.sensor import RestData
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
        if 'days_to_track' in sensor:
            i = 0
            while i <= sensor['days_to_track']:
                for allergen in sensor['allergens']:
                    add_devices([PollenkollSensor(rest, name, sensor, allergen, i)], True)
                i += 1
        else:
            for allergen in sensor['allergens']:
                add_devices([PollenkollSensor(rest, name, sensor, allergen, 0)], True)


# pylint: disable=no-member
class PollenkollSensor(Entity):
    """Representation of a PVOutput sensor."""

    def __init__(self, rest, name, sensor, allergen, day):
        """Initialize a PVOutput sensor."""
        self._rest = rest
        self._item = sensor
        self._city = sensor['city']
        self._state = None
        if 'hide_city_in_frontend' in sensor:
            if sensor['hide_city_in_frontend']:
                self._name = "Pollennivå " + allergen + " day" + str(day)
            else:
                self._name = "Pollennivå " + sensor['city'] + " " + allergen + " day" + str(day)
        else:
            self._name = "Pollennivå " + sensor['city'] + " " + allergen + " day" + str(day)
        self._day = day
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

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return '​'

    def update(self):
        """Get the latest data from the PVOutput API and updates the state."""
        try:
            pollen = {}
            self._rest.update()
            self._result = json.loads(self._rest.data)

            for datapart in self._result:
                CitiesData = datapart['CitiesData'];

            for city in CitiesData:
                if city['name'] in self._city:
                    pollen = city['pollen'];

            self._pollen = {}

            for allergen in pollen:
                if allergen['type'] == self._allergen:
                    if allergen['day' + str (self._day) + '_value'] == 'i.h.':
                        value = 0;
                    elif allergen['day' + str (self._day) + '_value'] == 'L':
                        value = 1;
                    elif allergen['day' + str (self._day) + '_value'] == 'L-M':
                        value = 2;
                    elif allergen['day' + str (self._day) + '_value'] == 'M':
                        value = 3;
                    elif allergen['day' + str (self._day) + '_value'] == 'M-H':
                        value = 4;
                    elif allergen['day' + str (self._day) + '_value'] == 'H':
                        value = 5;
                    elif allergen['day' + str (self._day) + '_value'] == 'H-H+':
                        value = 6;
                    self._state = value
                    self._pollen.update({"Dag": allergen['day' + str (self._day) + '_relative_date'] + ", " + allergen['day' + str (self._day) + '_name'] + " (" + allergen['day' + str (self._day) + '_date'] + ")", "Beskrivning": allergen['day' + str (self._day) + '_desc']})

        except TypeError as e:
            self._result = None
            _LOGGER.error(
                "Unable to fetch data from Pollenkoll. " + str(e))
