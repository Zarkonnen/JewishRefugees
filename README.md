# Mapping the fates of Jewish refugees in the 20th century

* [Online Version](https://zarkonnen.github.io/JewishRefugees/index.html)
* [Website](http://make.opendata.ch/wiki/project:vsjfrefugees_migration)

### Technical details
#### Setup
To work properly, the project must be hosted on a web server. The easiest way of doing this is to run server.py, which will then serve the project at `http://localhost:8000/`.

#### Source Data
The main data is stored in data.tsv, as a record of places and times. In addition, colorcodes.json defines the colors used for different kinds of places, eg hospitals are green and KZs black. important_events.tsv lists historically relevant events. famous_people.json lists the fates of some individual people.

#### Derived Data
Locations are geocoded using Google APIs, and cached in geocodes.tsv to prevent hitting rate limits. To re-code data.tsv, invoke `python geocode.py code data.tsv`. To see which geocodes are missing, invoke `python geocode.py list data.tsv`. In practice, some locations need to be geocoded by hand due to spelling errors or changes in place names.

The primary data, geocoded locations and color codes are then processed by clusters.py into clusters.json, a large data file that drives the display of information.
