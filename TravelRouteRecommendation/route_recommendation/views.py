from django.http.response import HttpResponsePermanentRedirect
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.http import HttpResponse
import requests
from django.views.decorators.csrf import csrf_protect
from pymongo import MongoClient
import xml.etree.ElementTree as ET
from utilities import Bbox
import re


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


def index(request):
    client = MongoClient()
    db = client.flickr
    seed_location = db.seed_location

    cities = []
    locations = seed_location.find()

    for loc in locations:
        cities.append({'id': loc['location_id'], 'name': loc['name']})

    return render(request, 'home.html', {'cities': cities})


def extract_landmarks(request):
    if not request.POST:
        return HttpResponseRedirect("/")

    location = request.POST.get('city')

    client = MongoClient()
    db = client.flickr
    clustersCollection = db.clusters
    photosCollection = db.photos

    pattern = "^" + str(location) + ".*$"
    regex = re.compile(pattern)
    _clusters = clustersCollection.find({"rank": {"$exists": True}, "cluster_id": regex, "poi_id": {"$ne": None}})

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
            'longitude': _cluster['longitude'],
            'poi_lat': _cluster['poi_lat'],
            'poi_lon': _cluster['poi_lon']
        }
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
        lat_center += float(_cluster['poi_lat'])
        lon_center += float(_cluster['poi_lon'])
        i += 1
        clusters.append(cluster)
    lat_center /= i
    lon_center /= i
    map_center = {
        'latitude': lat_center,
        'longitude': lon_center
    }
    client.close()
    return render(request, 'landmarks.html', {'clusters': clusters, 'map_center': map_center, 'location': location})


def get_route(request):

    if not request.POST:
        return HttpResponseRedirect("/")

    source = request.POST.get('source')
    dest = request.POST.get('dest')
    location = request.POST.get('city')

    client = MongoClient()
    db = client.flickr
    _routes = db.routes
    _node_data = db.node_data
    _clusters = db.clusters

    source_cluster = _clusters.find_one({'cluster_id': source})
    dest_cluster = _clusters.find_one({'cluster_id': dest})

    _source_node = _node_data.find_one({'node_id': source_cluster['poi_id']})
    _dest_node = _node_data.find_one({'node_id': dest_cluster['poi_id']})

    source_node = {
        'latitude': _source_node['lon_lat'][1],
        'longitude': _source_node['lon_lat'][0],
        'name': source_cluster['address']
    }
    dest_node = {
        'latitude': _dest_node['lon_lat'][1],
        'longitude': _dest_node['lon_lat'][0],
        'name': dest_cluster['address']
    }

    node_list = _node_data.find({'location': int(source[0])})
    node_dict = {}

    for node in node_list:
        node_dict[node['node_id']] = node['lon_lat']

    route = _routes.find_one({'source_cluster': source, 'dest_cluster': dest})
    if not route:
        return render(request, 'route_error.html', {'source': source_cluster['address'], 'destination': dest_cluster['address']})
    path = route['route']
    path_nodes = []

    for node_id in path:
        node = node_dict.get(node_id, None)
        if node:
            coords = [float(node[1]), float(node[0])]
            path_nodes.append(coords)

    lat_center = (source_node['latitude']+dest_node['latitude'])/2.0
    lon_center = (source_node['longitude']+dest_node['longitude'])/2.0
    map_center = {
        'latitude': lat_center,
        'longitude': lon_center
    }

    client.close()
    return render(request, 'route.html', {'source': source_node, 'dest': dest_node, 'path': path_nodes, 'map_center': map_center, 'location': location})


def rate(request):
    if not request.POST:
        return HttpResponseRedirect("/")

    client = MongoClient()
    db = client.flickr
    ratings = db.ratings

    rating = request.POST.get('rating')
    location = request.POST.get('location')

    print rating
    print location

    rating = {
        'location': location,
        'rating': rating
    }

    ratings.insert(rating)

    client.close()

    return HttpResponse("Done")


