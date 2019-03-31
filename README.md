# Home Assistant Pollennivå

Support for getting current pollen levels from pollenkoll.se
Visit https://pollenkoll.se/pollenprognos/ to find available cities

Place the folder `pollenkoll` in `<HA_CONFIG_DIR>/custom_components`
Add configuration to your `configuration.yaml`

This will create sensors named `senson.pollenniva_CITY_ALLERGEN` or `senson.pollenniva_ALLERGEN` based on 'hide_city_in_frontend: True'. The state will be the current level of that allergen.

Example configuration

```
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
```
