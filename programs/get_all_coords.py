# this file is to make sure that all the nodes in ways have latitude and longitude information

from pymongo import MongoClient
import xml.etree.ElementTree as ET
import requests
import overpy


def get_nodes_coords(location):

	api = overpy.Overpass()

	client = MongoClient()
	db = client.flickr
	# _node_data = db.node_data
	# _way_data = db.way_data
	if location==1:
		_node_data = db.node_data
		_way_data = db.way_data
	elif location==2:
		_node_data = db.node_data_2
		_way_data = db.way_data_2
	elif location==3:
		_node_data = db.node_data_3
		_way_data = db.way_data_3
	elif location==4:
		_node_data = db.node_data_4
		_way_data = db.way_data_4
	elif location==5:
		_node_data = db.node_data_5
		_way_data = db.way_data_5
	elif location==6:
		_node_data = db.node_data_6
		_way_data = db.way_data_6

	way_list = _way_data.find({'location': location, 'done': {'$exists': False}})
	# way_list = _way_data.find({'location': location})
	node_list = _node_data.find({'location': location})
	
	node_dict = {}
	xml_queries = []

	for node in node_list:
		node_dict[node['node_id']] = 1

	print "Node dict length: ", len(node_dict)

	nodes_to_query = {}

	for way in way_list:
		for node in way['node_list']:
			if node_dict.get(node, None) is None:
				if nodes_to_query.get(node, None) is None:
					nodes_to_query[node] = 0

	print "No of nodes to be queried: ", len(nodes_to_query)

	if not nodes_to_query:
		client.close()
		return

	count = 0
	for node in nodes_to_query:
		if count == 0:
			root = ET.Element('osm-script')

		id_query_elem = ET.SubElement(root, 'id-query', {'ref': node, 'type': 'node'})
		print_elem = ET.SubElement(root, 'print')
		count += 1

		if count == 30000:
			xml_queries.append((ET.tostring(root), count))
			count = 0

	xml_queries.append((ET.tostring(root), count))

	print "No of queries: ", len(xml_queries)
	print ""

	query_counter = 0

	for query in xml_queries:
		nodes_to_insert = []
		query_counter += 1
		print "Query ", query_counter, ": ", query[1]
		
		result = api.query(query[0])
		
		for node in result.nodes:
			node_id = str(node.id)
			if nodes_to_query.get(node_id, None) is None:
				continue
			if nodes_to_query[node_id] == 0:
				node_doc = {
					'node_id': node_id,
					'lon_lat': [float(node.lon), float(node.lat)],
					'location': location,
					'is_poi': False
				}
				nodes_to_insert.append(node_doc)
				nodes_to_query[node_id] = 1

		if len(nodes_to_insert) > 0:
			print len(nodes_to_insert)
			_node_data.insert(nodes_to_insert)

	client.close()


if __name__=='__main__':
	get_nodes_coords(2)