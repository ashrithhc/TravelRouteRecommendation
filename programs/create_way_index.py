from pymongo import MongoClient
from rtree import index


def rtree_indexing(location):
	try:

		client = MongoClient()
		db = client.flickr
		_way_data = db.way_data
		_node_data = db.node_data

		way_list = _way_data.find({})

		node_to_way_map = {}
		print "Begin creating a map"
		for way in way_list:
			for node in way['node_list']:
				if node_to_way_map.get(node, None) is None:
					node_to_way_map[node] = way['way_id']
		print "End creating a map"
		print len(node_to_way_map)


		prop = index.Property()
		prop.overwrite = True
		index_file = "index_ways_" + str(location)
		idx = index.Index(index_file, interleaved=False, properties=prop)

		_id = 1

		node_list = _node_data.find()

		for node in node_list:
			node_to_way = node_to_way_map.get(node['node_id'], None)
			if node_to_way is not None:
				lon_lat = node['lon_lat']
				latitude = float(lon_lat[1])
				longitude = float(lon_lat[0])
				idx.insert(_id, (latitude, latitude, longitude, longitude), obj={
						'node_id': node['node_id'],
						'way_id': node_to_way,
						'lon_lat': lon_lat
					})
				_id += 1

		print _id

		idx.close()

		client.close()

	except Exception as e:
		print(e)


if __name__=='__main__':
	rtree_indexing(1)