from pymongo import MongoClient
from imposm.parser import OSMParser
import time
from definitions import node_tags


def populate_data(node_id, tags, lon_lat, node_flag, category, location):
	try:

		client = MongoClient()
		db = client.flickr
		# _node_data = db.node_data
		if location==1:
			_node_data = db.node_data
		elif location==2:
			_node_data = db.node_data_2
		elif location==3:
			_node_data = db.node_data_3
		elif location==4:
			_node_data = db.node_data_4
		elif location==5:
			_node_data = db.node_data_5
		elif location==6:
			_node_data = db.node_data_6

		node = {
			"node_id" : str(node_id),
			"tags" : tags,
			"lon_lat" : lon_lat,
			"is_poi" : node_flag,
			"location" : location
		}

		if category is not None:
			node['category'] = category

		_node_data.insert(node)
	
		client.close()

	except Exception as e:
		print(e)

def check_poi(tags):
	for tag in node_tags:
		if tag in tags:
			categories = node_tags[tag]
			for category in categories:
				if tags[tag] in categories[category]:
					return category
			return '3'
	return None

def nodes_call(nodes):
    for node_id, tags, lon_lat in nodes:

    	#mongo doesn't allow '.' in its keys. So replace dots with underscore
    	for tag in tags:
    		if '.' in tag:
    			new_tag = tag.replace('.','_')
    			tags[new_tag] = tags.pop(tag)

    	category = check_poi(tags)
    	if category is None:
    		node_flag = False
    	else:
    		node_flag = True
    	# populate_data(node_id, tags, lon_lat, node_flag, category, 1)
    	populate_data(node_id, tags, lon_lat, node_flag, category, 2)
    	# populate_data(node_id, tags, lon_lat, node_flag, category, 3)
    	# populate_data(node_id, tags, lon_lat, node_flag, category, 4)
    	# populate_data(node_id, tags, lon_lat, node_flag, category, 5)
    	# populate_data(node_id, tags, lon_lat, node_flag, category, 6)


print "Calling parser\n"

parser = OSMParser(concurrency=4, nodes_callback=nodes_call)

# parser.parse('../osm_data/Sydney.osm.bz2')
parser.parse('../osm_data/Paris.osm.bz2')
# parser.parse('../osm_data/London.osm.bz2')
# parser.parse('../osm_data/Singapore.osm.bz2')
# parser.parse('../osm_data/NewYork.osm.bz2')
# parser.parse('../osm_data/SanFrancisco.osm.bz2')