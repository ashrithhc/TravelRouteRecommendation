import requests
import xml.etree.ElementTree as ET
from pymongo import MongoClient
from bbox import Bbox
from definitions import node_tags

def get_closest_poi(left, bottom, right, top):
    try:
        url = "http://open.mapquestapi.com/xapi/api/0.6/node[amenity=*][bbox=%s,%s,%s,%s]" % (left, bottom, right, top)
        decode = requests.get(url)

        root = ET.fromstring(decode.content)

        poi = None
        poi_tags = None
        top_category = 4
        poi_id = poi_name = lat = lon = None

        for element in root.findall('*'):
            name = None
            amenity = ""
            category = 4
            tags = element.findall('*')
            for tag in tags:
                key_value = tag.attrib
                if key_value['k'] == 'name':
                    name = key_value['v']
                if key_value['k'] == 'amenity':
                    amenity = key_value['v']
                    if amenity in node_tags['amenity']['1']:
                        category = 1
                    elif amenity in node_tags['amenity']['2']:
                        category = 2
                    elif amenity in node_tags['amenity']['2']:
                        category = 3

            if name is not None and category <= top_category:
                top_category = category
                poi = element
                poi_name = name

        if poi is not None:
            element_attributes = poi.attrib
            lat = float(element_attributes['lat'])
            lon = float(element_attributes['lon'])
            poi_id = element_attributes['id']
            poi_name = poi_name.encode('utf-8')

        return poi_name, poi_id, lat, lon

    except Exception as e:
        print(e)
        return None, None, None


def reverse_geocode():
    try:
        client = MongoClient()
        db = client.flickr
        clustersCollection = db.clusters
        clusters = clustersCollection.find({})

        for cluster in clusters:
            lat = cluster['latitude']
            lon = cluster['longitude']
            bbox = Bbox()

            bottom, left, top, right = bbox.boundingBox(lat, lon, 0.05)
            poi, poi_id, poi_lat, poi_lon = get_closest_poi(left, bottom, right, top)

            if poi is None:
                bottom, left, top, right = bbox.boundingBox(lat, lon, 0.1) #left_lat, left_lon, right_lat, right_lon
                poi, poi_id, poi_lat, poi_lon = get_closest_poi(left, bottom, right, top)
                
                if poi is None:
                    bottom, left, top, right = bbox.boundingBox(lat, lon, 0.2) #left_lat, left_lon, right_lat, right_lon
                    poi, poi_id, poi_lat, poi_lon = get_closest_poi(left, bottom, right, top)

                    if poi is None:
                        bottom, left, top, right = bbox.boundingBox(lat, lon, 0.5) #left_lat, left_lon, right_lat, right_lon
                        poi, poi_id, poi_lat, poi_lon = get_closest_poi(left, bottom, right, top)

            print cluster['cluster_id'], poi, poi_id, poi_lat, poi_lon

            clustersCollection.update({"cluster_id": cluster["cluster_id"]}, {"$set": {"address": poi, "poi_id": poi_id, "poi_lat": poi_lat, "poi_lon": poi_lon}})

        client.close()

    except Exception as e:
        print(e)

if __name__=='__main__':
    reverse_geocode()