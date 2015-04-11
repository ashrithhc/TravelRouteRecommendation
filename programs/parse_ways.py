from pymongo import MongoClient
from imposm.parser import OSMParser
import time
from definitions import way_tags

def populate_data(way_id, tags, node_list, way_flag, location):
	try:

		client = MongoClient()
		db = client.flickr
		# _way_data = db.way_data
		# _node_data = db.node_data
		if location==1:
			_way_data = db.way_data
		elif location==2:
			_way_data = db.way_data_2
		elif location==3:
			_way_data = db.way_data_3
		elif location==4:
			_way_data = db.way_data_4
		elif location==5:
			_way_data = db.way_data_5
		elif location==6:
			_way_data = db.way_data_6

		node_list = map(str,node_list)

		way = {
			"way_id" : str(way_id),
			"tags" : tags,
			"node_list" : node_list,
			"location": location
		}

		_way_data.insert(way)

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
    		# populate_data(way_id, tags, node_list, way_flag, 1)
    		populate_data(way_id, tags, node_list, way_flag, 2)
    		# populate_data(way_id, tags, node_list, way_flag, 3)
    		# populate_data(way_id, tags, node_list, way_flag, 4)
    		# populate_data(way_id, tags, node_list, way_flag, 5)
    		# populate_data(way_id, tags, node_list, way_flag, 6)


print "Calling parser\n"

parser = OSMParser(concurrency=4, ways_callback=ways_call)

# parser.parse('../osm_data/Sydney.osm.bz2')
parser.parse('../osm_data/Paris.osm.bz2')
# parser.parse('../osm_data/London.osm.bz2')
# parser.parse('../osm_data/Singapore.osm.bz2')
# parser.parse('../osm_data/NewYork.osm.bz2')
# parser.parse('../osm_data/SanFrancisco.osm.bz2')