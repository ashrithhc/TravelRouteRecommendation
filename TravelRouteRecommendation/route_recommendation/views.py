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


# tags to suggest similar landmarks
similarity_tags = [
    ['amenity|arts_centre', 'amenity|library', 'building|cathedral', 'historic|archaeological_site', 'tourism|artwork', 'tourism|gallery', 'tourism|museum'],
    ['building|cathedral', 'building|church', 'building|chapel', 'building|mosque', 'building|temple', 'building|synagogue', 'building|shrine'],
    ['shop|alcohol', 'shop|bakery', 'shop|beverages', 'shop|butcher', 'shop|cheese', 'shop|chocolate', 'shop|coffee', 'shop|confectionery', 'shop|convenience', 'shop|deli', 'shop|dairy', 'shop|farm', 'shop|greengrocer', 'shop|pasta', 'shop|pastry', 'shop|seafood', 'shop|tea', 'shop|wine', 'shop|department_store', 'shop|general', 'shop|kiosk', 'shop|mall', 'shop|supermarket'],
    ['amenity|cinema', 'amenity|theatre'],
    ['sport|9pin', 'sport|10pin', 'sport|archery', 'sport|base', 'sport|billiards', 'sport|bmx', 'sport|bobsleigh', 'sport|boules', 'sport|bowls', 'sport|canoe', 'sport|cliff_diving', 'sport|climbing', 'sport|climbing_adventure', 'sport|cockfighting', 'sport|croquet', 'sport|curling', 'sport|cycling', 'sport|darts', 'sport|dog_racing', 'sport|equistrian', 'sport|fencing', 'sport|free_flying', 'sport|horse_racing', 'sport|ice_skating', 'sport|karting', 'sport|kitesurfing', 'sport|motor', 'sport|motorcross', 'sport|paragliding', 'sport|racquet', 'sport|rc_car', 'sport|roller_skating', 'sport|rowing', 'sport|sailing', 'sport|scuba_diving', 'sport|shooting', 'sport|skateboard', 'sport|skiing', 'sport|surfing', 'sport|table_tennis', 'sport|swimming', 'sport|toboggan', 'sport|water_ski'],
    ['leisure|dog_park', 'leisure|firepit', 'leisure|hackerspace', 'leisure|playground', 'leisure|summer_camp', 'leisure|swimming_pool', 'leisure|track'],
    ['amenity|bar', 'amenity|bbq', 'amenity|biergarten', 'amenity|cafe', 'amenity|drinking_water', 'amenity|fast_food', 'amenity|food_court', 'amenity|ice_cream', 'amenity|pub', 'amenity|restaurant', 'amenity|nightclub', 'amenity|gambling', 'amenity|casino', 'amenity|swingerclub'],
    ['amenity|college', 'amenity|kindergarten', 'amenity|library', 'amenity|public_bookcase', 'amenity|school', 'amenity|university', 'amenity|bicycle_parking', 'amenity|bicycle_repair_station', 'amenity|bicycle_rental', 'amenity|boat_sharing', 'amenity|bus_station', 'amenity|car_rental', 'amenity|car_sharing', 'amenity|car_wash', 'amenity|charging_station', 'amenity|ferry_terminal', 'amenity|fuel', 'amenity|grit_bin', 'amenity|parking', 'amenity|parking_entrance', 'amenity|parking_space', 'amenity|taxi', 'amenity|atm', 'amenity|bank', 'amenity|bureau_de_change', 'amenity|baby-hatch', 'amenity|clinic', 'amenity|dentist', 'amenity|doctors', 'amenity|hospital', 'amenity|nursing_home', 'amenity|pharmacy', 'amenity|social_facility', 'amenity|veterinary', 'amenity|animal_boarding', 'amenity|animal_shelter', 'amenity|bench', 'amenity|clock', 'amenity|courthouse', 'amenity|coworking_space', 'amenity|crematorium', 'amenity|crypt', 'amenity|dojo', 'amenity|embassy', 'amenity|fire_station', 'amenity|grave_yard', 'amenity|gym', 'amenity|hunting_stand', 'amenity|game_feeding', 'amenity|marketplace', 'amenity|photo_booth', 'amenity|place_of_worship', 'amenity|police', 'amenity|post_box', 'amenity|post_office', 'amenity|prison', 'amenity|ranger_station', 'amenity|register_office', 'amenity|recycling', 'amenity|rescue_station', 'amenity|sauna', 'amenity|shelter', 'amenity|shower', 'amenity|telephone', 'amenity|toilets', 'amenity|townhall', 'amenity|vending_machine', 'amenity|waste_basket', 'amenity|waste_disposal', 'amenity|watering_place', 'amenity|water_point'],
    ['building|hotel', 'tourism|hotel'],
    ['historic|archaeological_site', 'historic|aircraft', 'historic|battlefield', 'historic|boundary_stone', 'historic|building', 'historic|castle', 'historic|cannon', 'historic|city_gate', 'historic|citywalls', 'historic|farm', 'historic|fort', 'historic|manor', 'historic|memorial', 'historic|monumnet', 'historic|optical_telegraph', 'historic|ruins', 'historic|rune_stone', 'historic|ship', 'historic|tomb', 'historic|wayside_cross', 'historic|wayside_shrine', 'historic|wreck'],
    ['building|apartments', 'building|farm', 'building|house', 'building|detached', 'building|residential', 'building|dormitory', 'building|terrace', 'building|houseboat', 'building|static_caravan', 'building|commercial', 'building|industrial', 'building|retail', 'building|warehouse', 'building|civic', 'building|hospital', 'building|school', 'building|stadium', 'building|train_station', 'building|transportation', 'building|university', 'building|barn', 'building|bridge', 'building|bunker', 'building|cabin', 'building|construction', 'building|cowshed', 'building|farm_auxiliary', 'building|garage', 'building|garages', 'building|greenhouse', 'building|hanger', 'building|hut', 'building|roof', 'building|shed', 'building|stable', 'building|sty', 'building|transformer_tower', 'building|ruins'],
    ['tourism|attraction', 'tourism|artwork', 'tourism|camp_site', 'tourism|gallery', 'tourism|museum', 'tourism|picnic_site', 'tourism|theme_park', 'tourism|viewpoint', 'tourism|zoo'],
    ['tourism|apartment', 'tourism|caravan_site', 'tourism|chalet', 'tourism|alpine_hut', 'tourism|guest_house', 'tourism|hostel', 'tourism|motel', 'tourism|information', 'tourism|wilderness_hut']
]


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
    reviewsCollection = db.reviews

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
        # cluster_points = []
        # points = [point for point in photosCollection.find({"cluster_info": cluster_no})]

        # if not points:
        #     continue
        #
        # for point in points:
        #     cluster_point = {
        #         'photo_id': point['photo_id'],
        #         'latitude': float(point['latitude']),
        #         'longitude': float(point['longitude']),
        #     }
        #     cluster_points.append(cluster_point)

        review = reviewsCollection.find_one({'cluster_id': cluster_no})
        photoExists = 0
        if review:
            rating = review['overall_rating']
            place_review = review.get('best_review')
            if not place_review:
                place_review = 'Review not available'
            if review.get('photo_exists', None):
                photoExists = 1
        else:
            rating = 'Not Available'
            place_review = 'Review not available'


        cluster = {
            'cluster_no': cluster_no,
            'cluster_loc': cluster_loc,
            # 'cluster_points': cluster_points,
            'color': colors[(i+1)%56],
            'cluster_address': cluster_address,
            'rank': _cluster['rank'],
            'review': place_review,
            'rating': rating,
            'photo_exists': photoExists
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
    request.session['clusters'] = clusters
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

    if location=='1':
        _node_data = db.node_data
    elif location=='2':
        _node_data = db.node_data_2
    elif location=='3':
        _node_data = db.node_data_3
    elif location=='4':
        _node_data = db.node_data_4
    elif location=='5':
        _node_data = db.node_data_5
    elif location=='6':
        _node_data = db.node_data_6
    clustersCollection = db.clusters
    reviewsCollection = db.reviews

    cluster_dict = {}
    review_dict = {}
    landmark_nodes = {}
    clusters = []

    if request.session.get('clusters', None):
        clusters = request.session['clusters']

    pattern = '^' + str(location) + '.*$'
    regex = re.compile(pattern)

    reviews = reviewsCollection.find({'cluster_id': regex})
    for review in reviews:
        review_dict[review['cluster_id']] = review

    _clusters = clustersCollection.find({"rank": {"$exists": True}, "cluster_id": regex, "poi_id": {"$ne": None}})

    for _cluster in _clusters:
        cluster_dict[_cluster['cluster_id']] = _cluster
        node = _node_data.find_one({'node_id': _cluster['poi_id']})
        node['cluster_address'] = _cluster['address']
        landmark_nodes[node['node_id']] = node

        if not clusters:
            cluster_no = _cluster['cluster_id']
            cluster_loc = {
                'latitude': _cluster['latitude'],
                'longitude': _cluster['longitude'],
                'poi_lat': _cluster['poi_lat'],
                'poi_lon': _cluster['poi_lon']
            }
            cluster_address = _cluster['address']

            review = review_dict[cluster_no]
            photoExists = 0
            if review:
                rating = review['overall_rating']
                place_review = review.get('best_review')
                if not place_review:
                    place_review = 'Review not available'
                if review.get('photo_exists', None):
                    photoExists = 1
            else:
                rating = 'Not Available'
                place_review = 'Review not available'


            cluster = {
                'cluster_no': cluster_no,
                'cluster_loc': cluster_loc,
                'cluster_address': cluster_address,
                'rank': _cluster['rank'],
                'review': place_review,
                'rating': rating,
                'photo_exists': photoExists
            }
            clusters.append(cluster)

    source_cluster = cluster_dict[source]
    dest_cluster = cluster_dict[dest]

    _source_node = landmark_nodes[source_cluster['poi_id']]
    _dest_node = landmark_nodes[dest_cluster['poi_id']]

    if not _source_node or not _dest_node:
        return render(request, 'route_error.html', {'source': source_cluster['address'], 'destination': dest_cluster['address']})

    review = review_dict[source]
    photoExists = 0
    if review:
        rating = review['overall_rating']
        place_review = review.get('best_review')
        if not place_review:
            place_review = 'Review not available'
        if review.get('photo_exists', None):
            photoExists = 1
    else:
        rating = 'Not Available'
        place_review = 'Review not available'

    source_node = {
        'latitude': _source_node['lon_lat'][1],
        'longitude': _source_node['lon_lat'][0],
        'name': source_cluster['address'],
        'photo_exists': photoExists,
        'review': place_review,
        'rating': rating,
        'cluster_no': source,
        'rank': source_cluster['rank']
    }

    review = review_dict[dest]
    photoExists = 0
    if review:
        rating = review['overall_rating']
        place_review = review.get('best_review')
        if not place_review:
            place_review = 'Review not available'
        if review.get('photo_exists', None):
            photoExists = 1
    else:
        rating = 'Not Available'
        place_review = 'Review not available'

    dest_node = {
        'latitude': _dest_node['lon_lat'][1],
        'longitude': _dest_node['lon_lat'][0],
        'name': dest_cluster['address'],
        'photo_exists': photoExists,
        'review': place_review,
        'rating': rating,
        'cluster_no': dest,
        'rank': dest_cluster['rank']
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

    similar_destinations = []

    dest_node_tags = _dest_node['tags']
    for tag in dest_node_tags:
        key_value = tag + "|" + dest_node_tags[tag]
        for category in similarity_tags:
            if key_value in category:
                for landmark in landmark_nodes.values():
                    landmark_tags = landmark['tags']
                    for landmark_tag in landmark_tags:
                        key_value_landmark = landmark_tag + "|" + landmark_tags[landmark_tag]
                        if key_value_landmark in category:
                            if landmark['node_id'] != _dest_node['node_id']:
                                similar_destinations.append(landmark)

    request.session['clusters'] = clusters
    client.close()
    return render(request, 'route.html', {'source': source_node, 'dest': dest_node, 'path': path_nodes, 'map_center': map_center, 'location': location, 'clusters': clusters, 'similar_destinations': similar_destinations})


def rate(request):
    if not request.POST:
        return HttpResponseRedirect("/")

    client = MongoClient()
    db = client.flickr
    ratings = db.ratings

    rating = request.POST.get('rating')
    location = request.POST.get('location')
    source = request.POST.get('source')
    destination = request.POST.get('destination')

    rating = {
        'location': location,
        'rating': rating,
        'source': source,
        'destination': destination
    }

    ratings.insert(rating)

    client.close()

    return HttpResponse("Done")


