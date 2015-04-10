# this file is to make sure that all the nodes in ways have latitude and longitude information

from pymongo import MongoClient
import xml.etree.ElementTree as ET
import requests
import overpy

def get_nodes(way_id, location):

	try:
		url = "http://api.openstreetmap.org/api/0.6/way/" + way_id + "/full"
		decode = requests.get(url)

		if not decode.content:
			return {}

		root = ET.fromstring(decode.content)
		nodes = {}

		for node in root.findall('node'):
			node_attrib = node.attrib
			node_id = node_attrib['id']
			lat = float(node_attrib['lat'])
			lon = float(node_attrib['lon'])
			_node = {
				'node_id': node_id,
				'lon_lat': [lon, lat],
				'is_poi': False,
				'location': location
			}
			nodes[node_id] = _node

		return nodes

	except Exception as e:
		print(e)
		return {}

def clean(location):
	try:
		client = MongoClient()
		db = client.flickr
		_node_data = db.node_data
		_way_data = db.way_data

		way_list = _way_data.find({'location': location, 'done': {'$exists': False}})

		node_list = _node_data.find({'location': location})
		node_dict = {}

		for node in node_list:
			node_dict[node['node_id']] = 1

		incomplete_ways = []

		count = 0
		for way in way_list:
			count += 1
			print count, " "
			for node in way['node_list']:
				if node_dict.get(node, None) is None:
					nodes_in_way = get_nodes(way['way_id'], location)
					for node_id in nodes_in_way:
						if node_dict.get(node_id, None) is None:
							_node_data.insert(nodes_in_way[node_id])
							node_dict[node_id] = 1
			_way_data.update({"way_id": way['way_id']}, {"$set": {"done": True}})

		client.close()

	except Exception as e:
		print(e)


if __name__=='__main__':
	# clean(1)
	pass