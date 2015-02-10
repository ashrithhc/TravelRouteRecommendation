from django.shortcuts import render
from django.http import HttpResponse
import mysql.connector
import requests
from mysql.connector.cursor import MySQLCursorDict
import json
from pymongo import MongoClient


def index(request):
    return HttpResponse("Hello, world. You're at the home page.")

# def to_address(lat, lon):
def to_address():
    mysql_config = {
        'user': 'root',
        'password': 'password',
        'host': '127.0.0.1',
        'database': 'flickr',
    }
    conn = mysql.connector.connect(**mysql_config)
    cursor = conn.cursor(cursor_class=MySQLCursorDict)
    query = "SELECT * FROM clusters"
    cursor.execute(query)

    rows = cursor.fetchall()
    for row in rows:
        lat = row['latitude']
        lon = row['longitude']
        url = "http://open.mapquestapi.com/geocoding/v1/reverse?key=Fmjtd%7Cluurn96z20%2C7x%3Do5-9w8a5u&location="
        url = url + str(lat) + "," + str(lon)
        decode = requests.get(url).json()
        print json.dumps(decode, indent=4, sort_keys=True)
        results = decode["results"]
        if results and len(results)>0:
            if results[0]["locations"]:
                country = results[0]["locations"][0]["adminArea1"].encode('utf-8')
                state = results[0]["locations"][0]["adminArea3"].encode('utf-8')
                county = results[0]["locations"][0]["adminArea4"].encode('utf-8')
                city = results[0]["locations"][0]["adminArea5"].encode('utf-8')
                postalcode = results[0]["locations"][0]["postalCode"].encode('utf-8')
                sideofstreet = results[0]["locations"][0]["sideOfStreet"].encode('utf-8')
                street = results[0]["locations"][0]["street"].encode('utf-8')
                Address = street + ', ' + sideofstreet + ', ' + city + ', ' + county + ', ' + state + ', ' + country + ', ' + postalcode

        query = "UPDATE clusters SET address = %s WHERE cluster_id = %s"
        cursor.execute(query, (Address,row['cluster_id']))
        conn.commit()
    conn.close()
    # return Address


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