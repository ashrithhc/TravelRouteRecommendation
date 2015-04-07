from pymongo import MongoClient
from sklearn.svm import SVC
import pickle

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

				first_road = _way_data.find_one({'way_id': closest_roads['first_road']})
				if first_road.get('n_poi_1', None):
					n_poi_11 = first_road['n_poi_1']
					n_poi_12 = first_road['n_poi_2']
					n_poi_13 = first_road['n_poi_3']
				else:
					n_poi_11 = _node_data.find({'belongs_to_way': closest_roads['first_road'], 'category': '1'}).count()
					n_poi_12 = _node_data.find({'belongs_to_way': closest_roads['first_road'], 'category': '2'}).count()
					n_poi_13 = _node_data.find({'belongs_to_way': closest_roads['first_road'], 'category': '3'}).count()
					_way_data.update({'way_id': closest_roads['first_road']}, {'$set': {'n_poi_1': n_poi_11, 'n_poi_2': n_poi_12, 'n_poi_3': n_poi_13}})

				second_road = _way_data.find_one({'way_id': closest_roads['second_road']})
				if second_road.get('n_poi_1', None):
					n_poi_21 = second_road['n_poi_1']
					n_poi_22 = second_road['n_poi_2']
					n_poi_23 = second_road['n_poi_3']
				else:
					n_poi_21 = _node_data.find({'belongs_to_way': closest_roads['second_road'], 'category': '1'}).count()
					n_poi_22 = _node_data.find({'belongs_to_way': closest_roads['second_road'], 'category': '2'}).count()
					n_poi_23 = _node_data.find({'belongs_to_way': closest_roads['second_road'], 'category': '3'}).count()
					_way_data.update({'way_id': closest_roads['second_road']}, {'$set': {'n_poi_1': n_poi_21, 'n_poi_2': n_poi_22, 'n_poi_3': n_poi_23}})			
			else:
				class_labels.append(1)
				dist1 = closest_roads['first_distance']

				first_road = _way_data.find_one({'way_id': closest_roads['first_road']})
				if first_road.get('n_poi_1', None):
					n_poi_11 = first_road['n_poi_1']
					n_poi_12 = first_road['n_poi_2']
					n_poi_13 = first_road['n_poi_3']
				else:
					n_poi_11 = _node_data.find({'belongs_to_way': closest_roads['first_road'], 'category': '1'}).count()
					n_poi_12 = _node_data.find({'belongs_to_way': closest_roads['first_road'], 'category': '2'}).count()
					n_poi_13 = _node_data.find({'belongs_to_way': closest_roads['first_road'], 'category': '3'}).count()
					_way_data.update({'way_id': closest_roads['first_road']}, {'$set': {'n_poi_1': n_poi_11, 'n_poi_2': n_poi_12, 'n_poi_3': n_poi_13}})
		else:
			class_labels.append(1)

		features = [dist1, dist2, n_poi_11, n_poi_21, n_poi_12, n_poi_22, n_poi_13, n_poi_23]
		features = map(float, features)

		training_set.append(features)

	client.close()

	return training_set, class_labels


def create_data_set():
	client = MongoClient()
	db = client.flickr
	_way_data = db.way_data
	_node_data = db.node_data

	node_list = _node_data.find({'is_poi': True, 'belongs_to_way': {'$exists': False}, 'closest_roads': {'$exists': True}})

	data_set = []
	nodes_order = []

	for node in node_list:
		dist1 = dist2 = n_poi_11 = n_poi_21 = n_poi_12 = n_poi_22 = n_poi_13 = n_poi_23 = 0.0
		closest_roads = node.get('closest_roads', None)
		dist1 = closest_roads['first_distance']
		dist2 = closest_roads['second_distance']

		first_road = _way_data.find_one({'way_id': closest_roads['first_road']})
		if first_road.get('n_poi_1', None):
			n_poi_11 = first_road['n_poi_1']
			n_poi_12 = first_road['n_poi_2']
			n_poi_13 = first_road['n_poi_3']
		else:
			n_poi_11 = _node_data.find({'belongs_to_way': closest_roads['first_road'], 'category': '1'}).count()
			n_poi_12 = _node_data.find({'belongs_to_way': closest_roads['first_road'], 'category': '2'}).count()
			n_poi_13 = _node_data.find({'belongs_to_way': closest_roads['first_road'], 'category': '3'}).count()
			_way_data.update({'way_id': closest_roads['first_road']}, {'$set': {'n_poi_1': n_poi_11, 'n_poi_2': n_poi_12, 'n_poi_3': n_poi_13}})

		second_road = _way_data.find_one({'way_id': closest_roads['second_road']})
		if second_road.get('n_poi_1', None):
			n_poi_21 = second_road['n_poi_1']
			n_poi_22 = second_road['n_poi_2']
			n_poi_23 = second_road['n_poi_3']
		else:
			n_poi_21 = _node_data.find({'belongs_to_way': closest_roads['second_road'], 'category': '1'}).count()
			n_poi_22 = _node_data.find({'belongs_to_way': closest_roads['second_road'], 'category': '2'}).count()
			n_poi_23 = _node_data.find({'belongs_to_way': closest_roads['second_road'], 'category': '3'}).count()
			_way_data.update({'way_id': closest_roads['second_road']}, {'$set': {'n_poi_1': n_poi_21, 'n_poi_2': n_poi_22, 'n_poi_3': n_poi_23}})
		
		features = [dist1, dist2, n_poi_11, n_poi_21, n_poi_12, n_poi_22, n_poi_13, n_poi_23]
		features = map(float, features)

		nodes_order.append(node['node_id'])
		data_set.append(features)

	client.close()

	return data_set, nodes_order


def normalize(training_set):
	training_set_transpose = [list(x) for x in zip(*training_set)]

	for i in xrange(len(training_set_transpose)):
		xmin = min(training_set_transpose[i])
		xmax = max(training_set_transpose[i])
		if xmin == 0 and xmax == 0:
			continue
		for j in xrange(len(training_set_transpose[i])):
			training_set_transpose[i][j] = float(training_set_transpose[i][j] - xmin)/float(xmax - xmin)

	training_set = [list(x) for x in zip(*training_set_transpose)]

	return training_set


def classify(training_set, class_labels):

	client = MongoClient()
	db = client.flickr
	_way_data = db.way_data
	_node_data = db.node_data

	classifier = SVC(cache_size=500)
	classifier.fit(training_set, class_labels)

	data_set, nodes_order = create_data_set()
	data_set = normalize(data_set)

	training_set_file = open('training_set_file.pkl', 'wb')
	class_labels_file = open('class_labels_file.pkl', 'wb')
	data_set_file = open('data_set_file.pkl', 'wb')

	pickle.dump(training_set, training_set_file)
	pickle.dump(class_labels, class_labels_file)
	pickle.dump(data_set, data_set_file)

	result_labels = classifier.predict(data_set)

	print result_labels
	print "\n\n"

	for i in xrange(len(result_labels)):
		node = _node_data.find_one({'node_id': nodes_order[i]})
		if result_labels[i]==1:
			belongs_to_way = node['closest_roads']['first_road']
		else:
			belongs_to_way = node['closest_roads']['second_road']
			
		# _node_data.update({'node_id': nodes_order[i]}, {'$set': {'belongs_to_way': belongs_to_way}})
		print node['node_id'], belongs_to_way

	client.close()
	training_set_file.close()
	data_set_file.close()
	class_labels_file.close()


if __name__=='__main__':
	training_set, class_labels = create_training_set()
	# training_set = [
	# 	[0,1,5,8],
	# 	[2,4,3,9],
	# 	[1,5,7,6]
	# ]
	training_set = normalize(training_set)

	classify(training_set, class_labels)
	# print training_set