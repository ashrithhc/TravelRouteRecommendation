from pymongo import MongoClient
from imposm.parser import OSMParser
import time

classifier_tags = ['highway', 'busway', 'route']

def populate_data(way_id, tags, node_list, way_flag):
	try:

		client = MongoClient()
		db = client.flickr
		_way_data = db.way_data
		_node_data = db.node_data

		way = {
			"way_id" : way_id,
			"tags" : tags,
			"node_list" : node_list,
			"is_road" : way_flag,
		}

		_way_data.insert(way)

		for node in node_list:
			_node = _node_data.find({'node_id': node})
			if(_node['is_poi'] == True)
			{
				_node_data.update({'node_id':node}, {'$set': {'belongs_to_way': way_id}})
				
			}

	
		client.close()

	except Exception as e:
		print(e)

def check_road(way_id, tags):
	for tag in classifier_tags:
		if tag in tags:
			return True
	return False

def ways_call(ways):
    for way_id, tags, node_list in ways:
    	way_flag = check_road(way_id, tags)
    	print way

    	populate_data(way_id, tags, node_list, way_flag)


print "Calling parser"
p = OSMParser(concurrency=4, ways_callback=ways_call)
p.parse('osm_data/singapore.osm.bz2')
# p.parse('osm_data/london_england.osm.bz2')
# p.parse('osm_data/singapore.osm.bz2')
# p.parse('osm_data/singapore.osm.bz2')
# p.parse('osm_data/singapore.osm.bz2')
# p.parse('osm_data/singapore.osm.bz2')