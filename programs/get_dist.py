#Get distance of non-assigned POIs to ways and consider the first two closest ways!

from pymongo import MongoClient
from bbox import Bbox
from haversine_distance import haversine

def get_two_roads(node_id, lon_lat, location):
	lat = lon_lat[1]
	lon = lon_lat[0]
	bbox = Bbox()
	left_lat, left_lon, right_lat, right_lon = bbox.boundingBox(lat, lon, 0.1)

	index_file = "index_ways_" + str(location)
	idx = index.Index(index_file)
	nodes_around = list(idx.intersection((left_lat, left_lon, right_lat, right_lon), objects="raw"))
	idx.close()

	#START
	#min_dist_1 will have the node with minimum distance, min_dist_2 will have the ode with next minimum distance.
	count = 0 #count=0 is to get min_dist_1, count = 1 is to get min_dist_2 avoiding nodes from same way.
	for i in range(len(nodes_around)):
		if count==0:
			min_dist_1 = dist_btw(lon_lat, nodes_around[i]['lon_lat'])
			min_way_1 = nodes_around[i]['way_id']
			count = count + 1

		elif count==1:
			min_dist_2 = dist_btw(lon_lat, nodes_around[i]['lon_lat'])
			d = min_dist_2
			min_way_2 = nodes_around[i]['way_id']
			if min_dist_2 < min_dist_1:
				min_dist_2 = min_dist_1
				min_way_2 = min_way_1
				min_dist_1 = d
				min_way_1 = nodes_around[i]['way_id']
			if min_way_1 != min_way_2:
				count = count + 1

		else:
			d = dist_btw(lon_lat, nodes_around[i]['lon_lat'])
			if d < min_dist_1 and nodes_around[i]['way_id'] != min_way_1:
				min_dist_2 = min_dist_1
				min_way_2 = min_way_1
				min_dist_1 = d
				min_way_1 = nodes_around[i]['way_id']
			elif d < min_dist_2 and nodes_around[i]['way_id'] != min_way_2:
				min_dist_2 = d
				min_way_2 = nodes_around[i]['way_id']
	#END

	return min_way_1, min_way_2


def check_nodes():
	try:

		client = MongoClient()
		db = client.flickr
		_way_data = db.way_data
		_node_data = db.node_data

		node_list = _node_data.find( {'belongs_to_way' : {'$exists' : False} })

		for node in node_list:
			node_tuple = _node_data.find({'node_id' : node['node_id']})
			way1, way2 = get_two_roads(node['node_id'], node_tuple['lon_lat'], 1)
			#use way1, way2 to assign node to a particular way.
	
		client.close()

	except Exception as e:
		print(e)