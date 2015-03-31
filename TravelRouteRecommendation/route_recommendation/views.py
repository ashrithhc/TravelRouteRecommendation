from django.shortcuts import render
from django.http import HttpResponse
import requests
from pymongo import MongoClient
import xml.etree.ElementTree as ET
from utilities import Bbox


def index(request):
    return HttpResponse("Hello, world. You're at the home page.")


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
            bottom, left, top, right = bbox.boundingBox(lat, lon, 0.1)
            poi = get_closest_poi(left, bottom, right, top)

        clustersCollection.update({"cluster_id": cluster["cluster_id"]}, {"$set": {"address": poi}})

    client.close()



def extract_landmarks(request, location='1'):
    client = MongoClient()
    db = client.flickr
    clustersCollection = db.clusters
    photosCollection = db.photos
    _clusters = clustersCollection.find({"content_score": {"$gte": 8}})

    if _clusters.count() == 0:
        return

    clusters = []
    colors = ["#FF0000", "#00FF00", "#0000FF", "#FFFF00", "#FF00FF", "#00FFFF", "#000000",
        "#800000", "#008000", "#000080", "#808000", "#800080", "#008080", "#808080",
        "#C00000", "#00C000", "#0000C0", "#C0C000", "#C000C0", "#00C0C0", "#C0C0C0",
        "#400000", "#004000", "#000040", "#404000", "#400040", "#004040", "#404040",
        "#200000", "#002000", "#000020", "#202000", "#200020", "#002020", "#202020",
        "#600000", "#006000", "#000060", "#606000", "#600060", "#006060", "#606060",
        "#A00000", "#00A000", "#0000A0", "#A0A000", "#A000A0", "#00A0A0", "#A0A0A0",
        "#E00000", "#00E000", "#0000E0", "#E0E000", "#E000E0", "#00E0E0", "#E0E0E0"]

    i = 0
    lat_center = 0.0
    lon_center = 0.0
    for _cluster in _clusters:
        cluster_no = _cluster['cluster_id']
        cluster_loc = {
            'latitude': _cluster['latitude'],
            'longitude': _cluster['longitude']
        }
        # cluster_address = to_address(cluster_loc['latitude'], cluster_loc['longitude'])
        cluster_address = _cluster['address']
        cluster_points = []
        points = [point for point in photosCollection.find({"cluster_info": cluster_no})]

        if not points:
            continue

        for point in points:
            cluster_point = {
                'photo_id': point['photo_id'],
                'latitude': float(point['latitude']),
                'longitude': float(point['longitude']),
            }
            cluster_points.append(cluster_point)

        cluster = {
            'cluster_no': cluster_no,
            'cluster_loc': cluster_loc,
            'cluster_points': cluster_points,
            'color': colors[(i+1)%56],
            'cluster_address': cluster_address,
            'rank': _cluster['rank']
        }
        lat_center += float(_cluster['latitude'])
        lon_center += float(_cluster['longitude'])
        i += 1
        clusters.append(cluster)
    lat_center /= i
    lon_center /= i
    map_center = {
        'latitude': lat_center,
        'longitude': lon_center
    }
    client.close()
    return render(request, 'landmarks.html', {'clusters': clusters, 'map_center': map_center})