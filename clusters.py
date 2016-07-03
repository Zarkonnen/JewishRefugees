import json

with open("colorcodes.json") as f:
    cluster_type_info = json.load(f)

cluster_type_by_name = {}
for ctype in cluster_type_info:
    for n in ctype["names"]:
        cluster_type_by_name[n] = ctype["color"]

geocodes = {}
with open("geocodes.tsv") as f:
    for l in f:
        l2 = l[:-1].split("\t")
        geocodes[l2[0]] = (float(l2[1]), float(l2[2]))

name_and_type = set()
locations = []
with open("data.tsv") as f:
    for l in f:
        l2 = l[:-1].split("\t")
        name = l2[1]
        typ = l2[5]
        if not name + typ in name_and_type:
            locations.append({"name": name, "type": typ, "position": geocodes[name]})
            name_and_type.add(name + typ)

def is_close(clusterA, clusterB, cluster_dist):
    aLat = sum(l["position"][0] for l in clusterA) / len(clusterA)
    aLng = sum(l["position"][1] for l in clusterA) / len(clusterA)
    bLat = sum(l["position"][0] for l in clusterB) / len(clusterB)
    bLng = sum(l["position"][1] for l in clusterB) / len(clusterB)
    return (aLat - bLat) * (aLat - bLat) + (aLng - bLng) * (aLng - bLng) < cluster_dist * cluster_dist
    
print "Locations:", len(locations)

clusters_info = {}
for zoom_level in range(2, 13):
    cluster_dist = pow(2, 11 - zoom_level) * 0.02
    clusters = [[x] for x in locations]
    progress = True
    while progress:
        progress = False
        i = 0
        while i < len(clusters):
            j = i + 1
            while j < len(clusters):
                clusterA = clusters[i]
                clusterB = clusters[j]
                if is_close(clusterA, clusterB, cluster_dist):
                    clusterA.extend(clusterB)
                    del clusters[j]
                    progress = True
                else:
                    j += 1
            i += 1
    print "Zoom", zoom_level, ":", str(len(clusters))
    zoom_level_info = []
    clusters_info[zoom_level] = zoom_level_info
    for c in clusters:
        name =  ", ".join(set(l["name"] for l in c))
        typ =  ", ".join(set(l["type"] for l in c))
        colorByMember = {l["name"] + l["type"]:cluster_type_by_name[l["type"].decode('utf-8')] for l in c}
        lat = sum(l["position"][0] for l in c) / len(c)
        lng = sum(l["position"][1] for l in c) / len(c)
        info = {}
        for l in c:
            typ = l["type"]
            if typ == "NULL":
                typ = "unbekannt"
            fontc = "white" if cluster_type_by_name[l["type"].decode('utf-8')].encode('utf-8') == "#000000" else "black"
            info[l["name"] + l["type"]] = ["<li style=\"background:" + cluster_type_by_name[l["type"].decode('utf-8')].encode('utf-8') + "; color: " + fontc + "\">", " " + l["name"] + ", " + typ + "</li>"]
        zoom_level_info.append({
            "name": name,
            "type": typ,
            "colorByMember": colorByMember,
            "lat": lat,
            "lng": lng,
            "members": list(set(l["name"] + l["type"] for l in c)),
            "info": info
        })
        
with open("clusters.json", "w") as f:
    f.write(json.dumps(clusters_info, indent=4))
