from django.shortcuts import render
from django.http import HttpResponse
import mysql.connector
from mysql.connector.cursor import MySQLCursorDict


def index(request):
    return HttpResponse("Hello, world. You're at the home page.")


def extract_landmarks(request, location='1'):
    mysql_config = {
        'user': 'root',
        'password': 'password',
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
        }
        clusters.append(cluster)
    if location=="1":
        return render(request, 'clusters.html', {'clusters': clusters})
    else:
        return render(request, 'landmarks.html', {'clusters': clusters})