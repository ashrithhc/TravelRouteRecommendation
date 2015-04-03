from pymongo import MongoClient

def assign():
	client = MongoClient()
	db = client.flickr
	_way_data = db.way_data
	_node_data = db.node_data

	print "Begin creating a map!"
	way_list = _way_data.find()

	node_to_way_map = {}

	for way in way_list:
		for node in way['node_list']:
			if node_to_way_map.get(node, None) is None:
				node_to_way_map[node] = way['way_id']

	print "End creating a map!"

	print "Begin assignment!"

	node_list = _node_data.find({'is_poi': True})
	count = 0

	for node in node_list:
		node_id = node['node_id']
		belongs_to_way = node_to_way_map.get(node_id, None)
		if belongs_to_way is not None:
			_node_data.update({'node_id': node_id}, {'$set': {'belongs_to_way': belongs_to_way}})
			count += 1
	print count
	print "End assignment!"

	client.close()


# function that assigns nodes to ways by looking at the street information present in the node and comparing it
# with the way name
def parse_node_tags():
	client = MongoClient()
	db = client.flickr
	_way_data = db.way_data
	_node_data = db.node_data

	# Create street name to way id dictionary

	print "Begin creating street name to way_id dictionary"

	street_to_way = {}
	way_list = _way_data.find()

	for way in way_list:
		tags = way['tags']
		for tag in tags:
			if 'name' in tag:
				if street_to_way.get(tags[tag], None) is None:
					street_to_way[tags[tag]] = way['way_id']

	print "End creating street name to way_id dictionary"

	print "Begin parsing node tags"

	node_list = _node_data.find({'$and': [{'belongs_to_way' : {'$exists' : False} }, {'is_poi': True}]})

	# count = 0
	for node in node_list:
		tags = node['tags']
		for tag in tags:
			if 'addr:street' in tag:
				belongs_to_way = street_to_way.get(tags[tag], None)
				if belongs_to_way is not None:
					_node_data.update({'node_id': node['node_id']}, {'$set': {'belongs_to_way': belongs_to_way}})
					# count += 1

	print "End parsing node tags"
	# print count

	client.close()

	
if __name__=='__main__':
	assign()
	parse_node_tags()
