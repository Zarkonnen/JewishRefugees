import requests, sys, json

api_key = "AIzaSyCQ8YLJ3J5CcGUBB9t9SdL-bSJRrbD_3po"
required_locations = set()
mode = sys.argv[1]

with open("individuals.json") as f:
    fp = json.load(f)
    for p in fp:
        for l in p["locations"]:
            required_locations.add(l["name"].encode('utf-8'))

with open("geocodes.tsv") as f:
    for l in f:
        location = l.split("\t")[0]
        if location in required_locations:
            required_locations.remove(location)

if mode == "code":
    print "Geocoding", len(required_locations), "new locations"

    with open("geocodes.tsv", "a") as f:
        for l in required_locations:
            print "Geocoding", l
            variations = [
                l.strip()
            ]
            for v in variations:
                r = requests.get("https://maps.googleapis.com/maps/api/geocode/json", params={"address":v.replace("/", ","), "key":"AIzaSyCQ8YLJ3J5CcGUBB9t9SdL-bSJRrbD_3po"})
                try:
                    lat = r.json()["results"][0]["geometry"]["location"]["lat"]
                    lng = r.json()["results"][0]["geometry"]["location"]["lng"]
                    f.write(l + "\t" + str(lat) + "\t" + str(lng) + "\n")
                    print "Found!"
                    break
                except Exception as e:
                    print e
                    print "Unable to geocode trying " + v                

if mode == "list":
    for l in required_locations:
        print l
    print len(required_locations)
