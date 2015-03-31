#Get distance of non-assigned POIs to ways and consider the first two closest ways!

from pymongo import MongoClient

def get_two_roads(node_id):
	

def check_nodes():
	try:

		client = MongoClient()
		db = client.flickr
		_way_data = db.way_data
		_node_data = db.node_data

		node_list = _node_data.find( {'belongs_to_way' : {'$exists' : False} })

		for node in node_list:
			get_two_roads(node['node_id'])
	
		client.close()

	except Exception as e:
		print(e)