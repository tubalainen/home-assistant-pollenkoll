# Home Assistant Pollennivå

Custom component for getting current pollen levels from pollenkoll.se
I started from https://github.com/JohNan/home-assistant-pollenkoll and tweaked it to behave as I wanted. His version gives you all allergens as attriutes on one single entity but I wanted one allergen per entity.

Visit https://pollenkoll.se/pollenprognos/ to find available cities

Place the folder `pollenkoll` in `<HA_CONFIG_DIR>/custom_components`
Add configuration to your `configuration.yaml`

This will create sensors named `senson.pollenniva_CITY_ALLERGEN` or `senson.pollenniva_ALLERGEN` depending on the presence of 'hide_city_in_frontend: True'. The state will be the current level of that allergen.

Example configuration

```
sensor:
  - platform: pollenkoll
    sensors:
      - city: Borlänge
        hide_city_in_frontend: True (OPTIONAL)
        days_to_track: 2 (OPTIONAL, possible values 0-3, 0 = today, 1 = today and tomorrow, 2 = today tomorrow and day after tomorrow and so on )
        allergens:
          - Al
          - Alm
          - Hassel
      - city: Jönköping
        hide_city_in_frontend: False (OPTIONAL)
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
