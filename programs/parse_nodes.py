from pymongo import MongoClient
from imposm.parser import OSMParser
import time

classifier_tags = ['amenity', 'building', 'historic', 'leisure', 'office', 'shop', 'tourism']

def populate_data(node_id, tags, lon_lat, node_flag, city_num):
	try:

		client = MongoClient()
		db = client.flickr
		_node_data = db.node_data

		node = {
			"node_id" : node_id,
			"tags" : tags,
			"lon_lat" : lon_lat,
			"is_poi" : node_flag,
			"location" : city_num
		}

		_node_data.insert(node)
	
		client.close()

	except Exception as e:
		print(e)

def check_poi(node_id, tags):
	for tag in classifier_tags:
		if tag in tags:
			return True
	return False

def nodes_call(nodes):
    for node_id, tags, lat_lon in nodes:
    	node_flag = check_poi(node_id, tags)
    	# print tags

    	populate_data(node_id, tags, lon_lat, node_flag, 3)


print "Calling parser"
p = OSMParser(concurrency=4, nodes_callback=nodes_call)
# p.parse('osm_data/singapore.osm.bz2')
p.parse('osm_data/london_england.osm.bz2')
# p.parse('osm_data/singapore.osm.bz2')
# p.parse('osm_data/singapore.osm.bz2')
# p.parse('osm_data/singapore.osm.bz2')
# p.parse('osm_data/singapore.osm.bz2')