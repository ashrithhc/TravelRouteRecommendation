from pymongo import MongoClient

way_dict = {}
w1 = 0.55
w2 = 0.35
w3 = 0.1

def assign_pois(location):
	try:

		client = MongoClient()
		db = client.flickr
		_way_data = db.way_data
		_node_data = db.node_data

		all_pois = _node_data.find({'location': location, 'is_poi': True, 'belongs_to_way': {'$exists': True}})

		for node in all_pois:
			if way_dict.get(node['belongs_to_way'], None) is None:
				way_dict[node['belongs_to_way']] = {'1':[], '2':[], '3':[]}
			else:
				way_dict[node['belongs_to_way']][node['category']].append(node['node_id'])


		print len(way_dict)
		client.close()

	except Exception as e:
		print(e)

def get_poi_usability(location):
	try:
		client = MongoClient()
		db = client.flickr
		_way_data = db.way_data

		for way in way_dict:
			way_pois = way_dict.get(way, None)
			if way_pois:
				poi_usability = (w1*len(way_pois['1']) + w2*len(way_pois['2']) + w3*len(way_pois['3']))
				_way_data.update({'way_id': way, 'location': location}, {'$set': {'poi_usability': poi_usability}})

		client.close()

	except Exception as e:
		print(e)


if __name__ == '__main__':
	location = 1
	assign_pois(location)
	get_poi_usability(location)
