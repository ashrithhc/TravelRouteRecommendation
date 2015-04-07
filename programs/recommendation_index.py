from pymongo import MongoClient

way_dict = {}

def assign_pois():
	try:

		client = MongoClient()
		db = client.flickr
		_way_data = db.way_data
		_node_data = db.node_data

		all_pois = _node_data.find({'is_poi' : True})

		for node in all_pois:
			if way_dict.get(node['way_id'], None) is None:
				way_dict[node['way_id']] = {'1':[], '2':[], '3':[]}
			else:
				way_dict[node['way_id']][node['category']].append(node['node_id'])


		client.close()

	except Exception as e:
		print(e)

def get_poi_index(way_id):
	return (w1*len(way_dict[way_id]['1']) + w2*len(way_dict[way_id]['2']) + w3*len(way_dict[way_id]['3']))

def get_recommendation_index(way_id):
	# pop = road_popularity(way_id)
	poi = get_poi_index(way_id)
	# leng = length_of_road(way_id)

	# return A1*pop + A2*poi - B*leng

if __name__ == 'main':
	assign_pois()