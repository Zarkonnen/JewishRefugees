import requests, sys

api_key = "AIzaSyCQ8YLJ3J5CcGUBB9t9SdL-bSJRrbD_3po"
required_locations = set()
mode = sys.argv[1]
for source_name in sys.argv[2:]:
    with open(source_name) as f:
        for l in f:
            required_locations.add(l.split("\t")[1])

with open("geocodes_switzerland.tsv") as f:
    for l in f:
        location = l.split("\t")[0]
        if location in required_locations:
            required_locations.remove(location)

if mode == "code":
    print "Geocoding", len(required_locations), "new locations"

    with open("geocodes_switzerland.tsv", "a") as f:
        for l in required_locations:
            print "Geocoding", l
            r = requests.get("https://maps.googleapis.com/maps/api/geocode/json", params={"address":l + ", Switzerland", "key":"AIzaSyCQ8YLJ3J5CcGUBB9t9SdL-bSJRrbD_3po"})
            try:
                lat = r.json()["results"][0]["geometry"]["location"]["lat"]
                lng = r.json()["results"][0]["geometry"]["location"]["lng"]
                f.write(l + "\t" + str(lat) + "\t" + str(lng) + "\n")
                print "Found!"
            except:
                print "Unable to geocode!"

if mode == "list":
    for l in required_locations:
        print l
