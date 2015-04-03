from pymongo import MongoClient

def assign():
	client = MongoClient()
	db = client.flickr
	_way_data = db.way_data
	_node_data = db.node_data

	print "Begin creating a map"
	way_list = _way_data.find()

	node_to_way_map = {}

	for way in way_list:
		for node in way['node_list']:
			if node_to_way_map.get(node, None) is None:
				node_to_way_map[node] = way['way_id']

	print "End creating a map"
	print len(node_to_way_map)
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

	client.close()
	

if __name__=='__main__':
	assign()