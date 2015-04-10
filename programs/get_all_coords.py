# this file is to make sure that all the nodes in ways have latitude and longitude information

from pymongo import MongoClient
import xml.etree.ElementTree as ET
import requests
import overpy


def get_nodes_coords(location):

	api = overpy.Overpass()

	client = MongoClient()
	db = client.flickr
	_node_data = db.node_data
	_way_data = db.way_data

	way_list = _way_data.find({'location': location, 'done': {'$exists': False}})
	node_list = _node_data.find({'location': location})
	
	node_dict = {}
	xml_queries = []

	for node in node_list:
		node_dict[node['node_id']] = 1

	count = 0
	for way in way_list:
		if count == 0:
			root = ET.Element('osm-script')
		for node in way['node_list']:
			if node_dict.get(node, None) is None:
				id_query_elem = ET.SubElement(root, 'id-query', {'ref': node, 'type': 'node'})
				print_elem = ET.SubElement(root, 'print')
				count += 1
		if count > 100000:
			count = 0
			xml_queries.append(ET.tostring(root))

	print "No of queries: ", len(xml_queries)
	print ""

	query_counter = 0

	for query in xml_queries:
		nodes_to_insert = []
		result = api.query(query)
		query_counter += 1
		print "Query ", query_counter
		for node in result.nodes:
			node_doc = {
				'node_id': node.id,
				'lon_lat': [float(node.lon), float(node.lat)],
				'location': location,
				'is_poi': False
			}
			nodes_to_insert.append(node_doc)

		_node_data.insert(nodes_to_insert)

	client.close()


if __name__=='__main__':
	get_nodes_coords(1)