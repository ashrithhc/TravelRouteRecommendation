#Get distance of non-assigned POIs to ways and consider the first two closest ways!

from pymongo import MongoClient
from bbox import Bbox
from haversine_distance import Haversine
from rtree import index


def dist_btw(lon_lat, way_id, node_list):
	
	point1 = {
		'latitude': lon_lat[1],
		'longitude': lon_lat[0]
	}
	min_dist = 0
	haversine = Haversine()

	for i in xrange(len(node_list)):
		point2 = {
			'latitude': node_list[i]['lon_lat'][1],
			'longitude': node_list[i]['lon_lat'][0]
		}

		if i == 0:
			min_dist = haversine.get_distance(point1, point2)
		else:
			dist = haversine.get_distance(point1, point2)
			if dist < min_dist:
				min_dist = dist

	return min_dist


def get_two_roads(node_id, lon_lat, location):
	lat = lon_lat[1]
	lon = lon_lat[0]
	bbox = Bbox()
	left_lat, left_lon, right_lat, right_lon = bbox.boundingBox(lat, lon, 0.7)

	index_file = "index_ways_" + str(location)
	idx = index.Index(index_file)
	nodes_around = list(idx.intersection((left_lat, left_lon, right_lat, right_lon), objects="raw"))
	idx.close()

	# Group all the nodes such that all nodes on a way occur together.
	close_ways = {}
	for node in nodes_around:
		if close_ways.get(node['way_id']) is None:
			close_ways[node['way_id']] = [node]
		else:
			close_ways[node['way_id']].append(node)

	#START
	#min_dist_1 will have the node with minimum distance, min_dist_2 will have the node with next minimum distance.
	count = 0 #count=0 is to get min_dist_1, count = 1 is to get min_dist_2 avoiding nodes from same way.
	min_way_1 = min_way_2 = min_dist_1 = min_dist_2 = None
	if len(close_ways) > 2:
		for way_id in close_ways:
			node_list = close_ways[way_id]
			if count==0:
				min_dist_1 = dist_btw(lon_lat, way_id, node_list)
				min_way_1 = way_id
				count = count + 1

			elif count==1:
				min_dist_2 = dist_btw(lon_lat, way_id, node_list)
				d = min_dist_2
				min_way_2 = way_id
				if min_dist_2 < min_dist_1:
					min_dist_2 = min_dist_1
					min_way_2 = min_way_1
					min_dist_1 = d
					min_way_1 = way_id
				count = count + 1

			else:
				d = dist_btw(lon_lat, way_id, node_list)
				if d < min_dist_1:
					min_dist_2 = min_dist_1
					min_way_2 = min_way_1
					min_dist_1 = d
					min_way_1 = way_id
				elif d < min_dist_2:
					min_dist_2 = d
					min_way_2 = way_id
	elif len(close_ways)==1:
		min_way_1 = close_ways.keys()[0]
		min_dist_1 = dist_btw(lon_lat, min_way_1, close_ways[min_way_1])
	#END

	return min_way_1, min_dist_1, min_way_2, min_dist_2


def check_nodes():
	try:

		client = MongoClient()
		db = client.flickr
		_way_data = db.way_data
		_node_data = db.node_data

		# node_list = _node_data.find({'$and': [{'belongs_to_way' : {'$exists' : False} }, {'is_poi': True}]})
		node_list = _node_data.find({'is_poi': True})
		for node in node_list:
			way1, dist1, way2, dist2 = get_two_roads(node['node_id'], node['lon_lat'], 1)
			#use way1, way2 to assign node to a particular way.
			if dist1 and dist1 <= 0.005:
				_node_data.update({'node_id': node['node_id']}, {'$set': {'belongs_to_way': way1}})

			elif way1:
				if way2:
					closest_roads = {
						'first_road': way1,
						'first_distance': dist1,
						'second_road': way2,
						'second_distance': dist2 
					}
					_node_data.update({'node_id': node['node_id']}, {'$set': {'closest_roads': closest_roads}})
				else:
					closest_roads = {
						'first_road': way1,
						'first_distance': dist1
					}
					_node_data.update({'node_id': node['node_id']}, {'$set': {'belongs_to_way': way1}})
					_node_data.update({'node_id': node['node_id']}, {'$set': {'closest_roads': closest_roads}})

		client.close()

	except Exception as e:
		print(e)


if __name__=='__main__':
	check_nodes()