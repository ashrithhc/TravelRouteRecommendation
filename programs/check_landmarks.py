from pymongo import MongoClient
import re

def check(location):

	client = MongoClient()
	db = client.flickr
	_clusters = db.clusters
	_node_data = db.node_data

	pattern = "^" + str(location) + ".*$"
	regex = re.compile(pattern)
	clusters = _clusters.find({"cluster_id": regex, "poi_id": {"$ne": None}, "rank": {"$exists": True}})

	count = 0
	for cluster in clusters:
		poi_id = cluster['poi_id']
		print poi_id
		node = _node_data.find_one({'node_id': poi_id})
		if not node or not node.get('belongs_to_way', None):
			count += 1

	print "Location: ", location
	print "Count: ", count
	print ""

	client.close()

if __name__=='__main__':
	location = 1
	check(location)