# Home Assistant Pollennivå

Custom component for getting current pollen levels from pollenkoll.se
This code started with https://github.com/simonfalun/home-assistant-pollenkoll and Simon forked it from https://github.com/JohNan/home-assistant-pollenkoll and tweaked it to behave a bit different. JonNans version gives you all allergens as attriutes on one single entity but I wanted one allergen per entity.

I also added a template sensor examples for presenting the pollen status in text.

This version is also adapted for Home Assistant 0.91 and above (Breaking changes)

Visit https://pollenkoll.se/pollenprognos/ to find available cities

Place the folder including the files `pollenkoll` in `<HA_CONFIG_DIR>/custom_components`
Add configuration to your `configuration.yaml`

This will create sensors named `senson.pollenniva_CITY_ALLERGEN` or `senson.pollenniva_ALLERGEN` depending on the presence of 'hide_city_in_frontend: True'. The state will be the current level of that allergen.

Example configuration

```
sensor:
  - platform: pollenkoll
    sensors:
      - city: Forshaga
        hide_city_in_frontend: False # Optional
        days_to_track: 2 # Optional
        allergens:
         - Al
         - Alm
         - Hassel
         - Björk
         - Gräs
         - Gråbo
         - Bok
         - Sälg/Vide
         - Ek
```
