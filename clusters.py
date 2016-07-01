geocodes = {}
with open("geocodes.tsv") as f:
    for l in f:
        l2 = l.split("\t")
        geocodes[l2[0]] = [float(l2[1]), float(l2[2])]

name_and_type = set()
locations = []
with open("data.tsv") as f:
    for l in f:
        l2 = l.split("\t")
        name = l2[1]
        typ = l2[5]
        if not name + typ in name_and_type:
            locations.append({"name": name, "type": typ, "position": geocodes[name]})
            name_and_type.add(name + typ)

print len(locations)
