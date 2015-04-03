from pymongo import MongoClient
from imposm.parser import OSMParser
import time
from definitions import way_tags

def populate_data(way_id, tags, node_list, way_flag):
	try:

		client = MongoClient()
		db = client.flickr
		_way_data = db.way_data
		_node_data = db.node_data

		node_list = map(str,node_list)

		way = {
			"way_id" : str(way_id),
			"tags" : tags,
			"node_list" : node_list,
			# "is_road" : way_flag,
		}

		_way_data.insert(way)

		# for node in node_list:
		# 	_node = _node_data.find_one({'node_id': node})
		# 	if _node and _node['is_poi'] == True:
		# 		_node_data.update({'node_id':node}, {'$set': {'belongs_to_way': way_id}})

		client.close()

	except Exception as e:
		print(e)

def check_road(tags):
	for tag in way_tags:
		if tag in tags:
			if tags[tag] in way_tags[tag]:
				return True
	return False

def ways_call(ways):
    for way_id, tags, node_list in ways:

    	#mongo doesn't allow '.' in its keys. So replace dots with underscore
    	for tag in tags:
    		if '.' in tag:
    			new_tag = tag.replace('.','_')
    			tags[new_tag] = tags.pop(tag)

    	way_flag = check_road(tags)
    	if way_flag:
    		populate_data(way_id, tags, node_list, way_flag)


print "Calling parser\n"

parser = OSMParser(concurrency=4, ways_callback=ways_call)

parser.parse('../osm_data/Sydney.osm.bz2')
# parser.parse('../osm_data/Paris.osm.bz2')
# parser.parse('../osm_data/London.osm.bz2')
# parser.parse('../osm_data/Singapore.osm.bz2')
# parser.parse('../osm_data/NewYork.osm.bz2')
# parser.parse('../osm_data/SanFrancisco.osm.bz2')