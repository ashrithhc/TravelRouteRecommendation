from itertools import tee, izip, islice
from networkx import DiGraph, shortest_path
from pymongo import MongoClient
from haversine_distance import Haversine
from sys import maxint
import requests
import xml.etree.ElementTree as ET
import re


nwise = lambda g,n=2: izip(*(islice(g,i,None) for i,g in enumerate(tee(g,n))))

class Graph:
	def __init__(self, location):
		self.edges = []
		self.graph = DiGraph()
		self.client = MongoClient()
		self.db = self.client.flickr
		self._way_data = self.db.way_data
		self._node_data = self.db.node_data
		self.location = location
		self.node_dict = {}

	def __del__(self):
		self.client.close()

	def build_graph(self):
		way_list = self._way_data.find({'location': self.location})
		node_list = self._node_data.find({'location': self.location})
		weight_min = maxint

		for node in node_list:
			self.node_dict[node['node_id']] = node['lon_lat']

		for way in way_list:
			poi_usability = way.get('poi_usability', 0)
			for segment in nwise(way['node_list']):
				dist = 0.0
				node1 = self.node_dict.get(segment[0], None)
				node2 = self.node_dict.get(segment[1], None)
				if node1 and node2:
					haversine = Haversine()
					dist = haversine.get_distance({'latitude': float(node1[1]), 'longitude': float(node1[0])}, {'latitude': float(node2[1]), 'longitude': float(node2[0])})

				weight = (0.7 * poi_usability) - (0.3 * dist)
				if weight < weight_min:
					weight_min = weight

				self.edges.append([segment[0], segment[1], weight])
		
		# file_name = "../output_files/edges_" + str(self.location) + ".txt"
		# edges_file = open(file_name, 'w')

		if weight_min < 0:	
			for i in xrange(len(self.edges)):
				self.edges[i][2] -= weight_min
				if self.edges[i][2] == 0:
					self.edges[i][2] = maxint
				else:
					self.edges[i][2] = 1.0/self.edges[i][2]

				# edges_file.write(" ".join(map(str, self.edges[i])))
				# edges_file.write("\n")
				self.graph.add_edge(self.edges[i][0], self.edges[i][1], weight = self.edges[i][2])
		else:	
			for i in xrange(len(self.edges)):
				if self.edges[i][2] == 0:
					self.edges[i][2] = maxint
				else:
					self.edges[i][2] = 1.0/self.edges[i][2]
				# edges_file.write(" ".join(map(str, self.edges[i])))
				# edges_file.write("\n")				
				self.graph.add_edge(self.edges[i][0], self.edges[i][1], weight = self.edges[i][2])

		# edges_file.close()


def get_nodes(node_id, location):
	try:
		url = "http://api.openstreetmap.org/api/0.6/node/" + node_id
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



if __name__ == '__main__':

	client = MongoClient()
	db = client.flickr
	_node_data = db.node_data
	_clusters = db.clusters
	_way_data = db.way_data
	_routes = db.routes

	location = 1
	graph_obj = Graph(location)

	graph_obj.build_graph()

	regex = re.compile("^1.*$")
	clusters = [cluster for cluster in _clusters.find({'cluster_id': regex, 'rank': {'$exists': True}, 'poi_id': {'$ne': None}})]

	for source in clusters:
		for dest in clusters:
			if source['cluster_id'] == dest['cluster_id']:
				continue

			source_poi = _node_data.find_one({'node_id': source['poi_id'], 'location': location})
			dest_poi = _node_data.find_one({'node_id': dest['poi_id'], 'location': location})
			source_way = _way_data.find_one({'way_id': source_poi['belongs_to_way'], 'location': location})
			dest_way = _way_data.find_one({'way_id': dest_poi['belongs_to_way'], 'location': location})
			source_node = source_way['node_list'][0]
			dest_node = dest_way['node_list'][0]

			print "\n\nSource cluster: ", source['cluster_id']
			print "Destination cluster: ", dest['cluster_id']
			print "Source: ", source_node
			print "Destination: ", dest_node

			# path = shortest_path(graph_obj.graph, "20827842", "14750536")
			try:
				path = shortest_path(graph_obj.graph, source_node, dest_node)

				count = 0
				for node in path:
					if graph_obj.node_dict.get(node, None):
						# print node, "Yes"
						continue
					else:
						# print node, "No"
						count += 1
						nodes = get_nodes(node, 1)
						for node_id in nodes:
							_node_data.insert(nodes[node_id])
							graph_obj.node_dict[node_id] = nodes[node_id]['lon_lat']
				route = {
					'source_cluster': source['cluster_id'],
					'dest_cluster': dest['cluster_id'],
					'source_way': source_way['way_id'],
					'dest_way': dest_way['way_id'],
					'route': path
				}

				_routes.insert(route)

				print "\nNo of nodes with geo info: ", len(path)-count
				print "No of nodes with no geo info: ", count
			except Exception as e:
				print e

	client.close()


