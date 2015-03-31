from pymongo import MongoClient

def rtree_indexing(location):
	try:

		client = MongoClient()
		db = client.flickr
		_way_data = db.way_data
		_node_data = db.node_data

		prop = index.Property()
		prop.overwrite = True
		index_file = "index_ways_" + str(location)
		idx = index.Index(index_file, interleaved=False, properties=prop)

		way_list = _way_data.find()

		_id = 1
		for way in way_list:
			node_list = way['node_list']

			for node in node_list:
				node_tuple = _node_data.find({'node_id' : node})
				lon_lat = node_tuple['lon_lat']

				latitude = float(lon_lat[1])
				longitude = float(lon_lat[0])
				idx.insert(_id, (latitude, latitude, longitude, longitude), obj={
						'node_id': node,
						'way_id': way['way_id'],
						'lon_lat': lon_lat
					})
				_id += 1

		idx.close()

		client.close()

	except Exception as e:
		print(e)


rtree_indexing(1)