import requests
import xml.etree.ElementTree as ET
from pymongo import MongoClient
from bbox import Bbox

def get_closest_poi(left, bottom, right, top):

    url = "http://open.mapquestapi.com/xapi/api/0.6/node[amenity=*][bbox=%s,%s,%s,%s]" % (left, bottom, right, top)
    decode = requests.get(url)
    root = ET.fromstring(decode.content)

    max_tags = 0
    poi = None
    poi_tags = None
    for element in root.findall('*'):
        name = False
        tags = element.findall('*')
        for tag in tags:
            key_value = tag.attrib
            if key_value['k'] == 'name':
                name = True
        if name and len(tags) > max_tags:
            max_tags = len(tags)
            poi = element
            poi_tags = tags

    poi_name = ""
    if poi is not None:
        for tag in poi_tags:
            key_value = tag.attrib
            if key_value['k'] == 'name':
                poi_name = key_value['v']

    return poi_name


def reverse_geocode():
    client = MongoClient()
    db = client.flickr
    clustersCollection = db.clusters
    clusters = clustersCollection.find({})

    for cluster in clusters:
        lat = cluster['latitude']
        lon = cluster['longitude']
        bbox = Bbox()
        bottom, left, top, right = bbox.boundingBox(lat, lon, 0.05)
        poi = get_closest_poi(left, bottom, right, top)
        if poi == "":
            bottom, left, top, right = bbox.boundingBox(lat, lon, 0.1) #left_lat, left_lon, right_lat, right_lon
            poi = get_closest_poi(left, bottom, right, top)

        clustersCollection.update({"cluster_id": cluster["cluster_id"]}, {"$set": {"address": poi}})
        break

    client.close()