from pymongo import MongoClient
import re
import requests

def get_reviews(location):
	client = MongoClient()
	db = client.flickr
	if location==1:
		_node_data = db.node_data
		_way_data = db.way_data
	elif location==2:
		_node_data = db.node_data_2
		_way_data = db.way_data_2
	elif location==3:
		_node_data = db.node_data_3
		_way_data = db.way_data_3
	elif location==4:
		_node_data = db.node_data_4
		_way_data = db.way_data_4
	elif location==5:
		_node_data = db.node_data_5
		_way_data = db.way_data_5
	elif location==6:
		_node_data = db.node_data_6
		_way_data = db.way_data_6
	_clusters = db.clusters
	_reviews = db.reviews

	pattern = "^" + str(location) + ".*$"
    regex = re.compile(pattern)
    clusters = _clusters.find({"rank": {"$exists": True}, "cluster_id": regex, "poi_id": {"$ne": None}})

    for cluster in clusters:
    	name = cluster['address']