from pymongo import MongoClient


# training set is a matrix of size [no_of_samples X no_of_features]
# features: dist1, dist2, n_poi_11, n_poi_21, n_poi_12, n_poi_22, n_poi_13, n_poi_23 
def create_training_set():
	client = MongoClient()
	db = client.flickr
	_way_data = db.way_data
	_node_data = db.node_data

	node_list = _node_data.find({'belongs_to_way': {'$exists' : True} })

	training_set = []
	class_labels = []

	for node in node_list:
		dist1 = dist2 = n_poi_11 = n_poi_21 = n_poi_12 = n_poi_22 = n_poi_13 = n_poi_23 = 0.0
		closest_roads = node.get('closest_roads', None)
		if closest_roads:
			if closest_roads.get('second_road', None) is not None:
				if node['belongs_to_way'] == closest_roads['second_road']:
					class_labels.append(-1)
				else:
					class_labels.append(1)
				dist1 = closest_roads['first_distance']
				dist2 = closest_roads['second_distance']
				n_poi_11 = _node_data.find({'belongs_to_way': closest_roads['first_road'], 'category': '1'}).count()
				n_poi_12 = _node_data.find({'belongs_to_way': closest_roads['first_road'], 'category': '2'}).count()
				n_poi_13 = _node_data.find({'belongs_to_way': closest_roads['first_road'], 'category': '3'}).count()
				n_poi_21 = _node_data.find({'belongs_to_way': closest_roads['second_road'], 'category': '1'}).count()
				n_poi_22 = _node_data.find({'belongs_to_way': closest_roads['second_road'], 'category': '2'}).count()
				n_poi_23 = _node_data.find({'belongs_to_way': closest_roads['second_road'], 'category': '3'}).count()
			else:
				class_labels.append(1)
				dist1 = closest_roads['first_distance']
				n_poi_11 = _node_data.find({'belongs_to_way': closest_roads['first_road'], 'category': '1'}).count()
				n_poi_12 = _node_data.find({'belongs_to_way': closest_roads['first_road'], 'category': '2'}).count()
				n_poi_13 = _node_data.find({'belongs_to_way': closest_roads['first_road'], 'category': '3'}).count()
		else:
			class_labels.append(1)

		features = [dist1, dist2, n_poi_11, n_poi_21, n_poi_12, n_poi_22, n_poi_13, n_poi_23]
		features = map(float, features)

		training_set.append(features)

	client.close()

	return training_set, class_labels


def normalize(training_set):
	training_set_transpose = [list(x) for x in zip(*training_set)]

	for i in xrange(len(training_set_transpose)):
		xmin = min(training_set_transpose[i])
		xmax = max(training_set_transpose[i])
		if xmin == 0 and xmax == 0:
			continue
		for j in xrange(len(training_set_transpose[i])):
			training_set_transpose[i][j] = float((training_set_transpose[i][j] - xmin)/(xmax - xmin))

	training_set = [list(x) for x in zip(*training_set_transpose)]

	return training_set


if __name__=='__main__':
	training_set, class_labels = create_training_set()
	training_set = normalize(training_set)

	print training_set