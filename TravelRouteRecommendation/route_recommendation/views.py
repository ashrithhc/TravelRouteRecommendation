from django.shortcuts import render
from django.http import HttpResponse
import mysql.connector
import requests
# from mysql.connector.cursor import MySQLCursorDict


def index(request):
    return HttpResponse("Hello, world. You're at the home page.")

def to_address(lat, lon):
    url = "http://open.mapquestapi.com/geocoding/v1/reverse?key=Fmjtd%7Cluurn96z20%2C7x%3Do5-9w8a5u&location="
    # lat = 40.053116
    # lon = -76.313603

    url = url + str(lat) + "," + str(lon)

    decode = requests.get(url).json()

    country = decode["results"][0]["locations"][0]["adminArea1"].encode()
    state = decode["results"][0]["locations"][0]["adminArea3"].encode()
    county = decode["results"][0]["locations"][0]["adminArea4"].encode()
    city = decode["results"][0]["locations"][0]["adminArea5"].encode()

    postalcode = decode["results"][0]["locations"][0]["postalCode"].encode()
    sideofstreet = decode["results"][0]["locations"][0]["sideOfStreet"].encode()
    street = decode["results"][0]["locations"][0]["street"].encode()

    Address = street + ', ' + sideofstreet + ', ' + city + ', ' + county + ', ' + state + ', ' + country + ', ' + postalcode

    return Address


def extract_landmarks(request, location='1'):
    mysql_config = {
        'user': 'root',
        'password': 'nopassword',
        'host': '127.0.0.1',
        'database': 'flickr',
    }
    conn = mysql.connector.connect(**mysql_config)
    cursor = conn.cursor(cursor_class=MySQLCursorDict)
    query = "SELECT * FROM clusters WHERE content_score > 10"
    cursor.execute(query)
    rows = cursor.fetchall()
    if not rows:
        return
    clusters = []
    for row in rows:
        cluster_no = row['cluster_id']
        cluster_loc = {
            'latitude': row['latitude'],
            'longitude': row['longitude']
        }
        cluster_address = to_address(cluster_loc['latitude'], cluster_loc['longitude'])
        cluster_points = []
        query = "select * from temp where cluster_info=%s"
        cursor.execute(query, (cluster_no,))
        points = cursor.fetchall()
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
            'cluster_address': cluster_address,
        }
        clusters.append(cluster)
    if location=="1":
        return render(request, 'clusters.html', {'clusters': clusters})
    else:
        return render(request, 'landmarks.html', {'clusters': clusters})