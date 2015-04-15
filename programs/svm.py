from pymongo import MongoClient
from sklearn.svm import SVC
import pickle

# training set is a matrix of size [no_of_samples X no_of_features]
# features: dist1, dist2, n_poi_11, n_poi_21, n_poi_12, n_poi_22, n_poi_13, n_poi_23 
def create_training_set(location):
	client = MongoClient()
	db = client.flickr
	# _way_data = db.way_data
	# _node_data = db.node_data
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

	way_dict = {}
	way_list = _way_data.find({'location': location, 'n_poi_1': {'$exists': True}})
	for way in way_list:
		way_dict[way['way_id']] = way

	node_list = list(_node_data.find({'belongs_to_way': {'$exists' : True}, 'location': location }))
	print "No of pois to be trained: ", len(node_list)

	training_set = []
	class_labels = []

	count = 0
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

				first_road = way_dict.get(closest_roads['first_road'], None)
				if not first_road:
					first_road = _way_data.find_one({'way_id': closest_roads['first_road'], 'location': location})
				if first_road.get('n_poi_1', None):
					n_poi_11 = first_road['n_poi_1']
					n_poi_12 = first_road['n_poi_2']
					n_poi_13 = first_road['n_poi_3']
				else:
					n_poi_11 = _node_data.find({'belongs_to_way': closest_roads['first_road'], 'category': '1', 'location': location}).count()
					n_poi_12 = _node_data.find({'belongs_to_way': closest_roads['first_road'], 'category': '2', 'location': location}).count()
					n_poi_13 = _node_data.find({'belongs_to_way': closest_roads['first_road'], 'category': '3', 'location': location}).count()
					_way_data.update({'way_id': closest_roads['first_road'], 'location': location}, {'$set': {'n_poi_1': n_poi_11, 'n_poi_2': n_poi_12, 'n_poi_3': n_poi_13}})

				second_road = way_dict.get(closest_roads['second_road'], None)
				if not second_road:
					second_road = _way_data.find_one({'way_id': closest_roads['second_road'], 'location': location})
				if second_road.get('n_poi_1', None):
					n_poi_21 = second_road['n_poi_1']
					n_poi_22 = second_road['n_poi_2']
					n_poi_23 = second_road['n_poi_3']
				else:
					n_poi_21 = _node_data.find({'belongs_to_way': closest_roads['second_road'], 'category': '1', 'location': location}).count()
					n_poi_22 = _node_data.find({'belongs_to_way': closest_roads['second_road'], 'category': '2', 'location': location}).count()
					n_poi_23 = _node_data.find({'belongs_to_way': closest_roads['second_road'], 'category': '3', 'location': location}).count()
					_way_data.update({'way_id': closest_roads['second_road'], 'location': location}, {'$set': {'n_poi_1': n_poi_21, 'n_poi_2': n_poi_22, 'n_poi_3': n_poi_23}})			
			else:
				class_labels.append(1)
				dist1 = closest_roads['first_distance']

				first_road = way_dict.get(closest_roads['first_road'], None)
				if not first_road:
					first_road = _way_data.find_one({'way_id': closest_roads['first_road'], 'location': location})
				if first_road.get('n_poi_1', None):
					n_poi_11 = first_road['n_poi_1']
					n_poi_12 = first_road['n_poi_2']
					n_poi_13 = first_road['n_poi_3']
				else:
					n_poi_11 = _node_data.find({'belongs_to_way': closest_roads['first_road'], 'category': '1', 'location': location}).count()
					n_poi_12 = _node_data.find({'belongs_to_way': closest_roads['first_road'], 'category': '2', 'location': location}).count()
					n_poi_13 = _node_data.find({'belongs_to_way': closest_roads['first_road'], 'category': '3', 'location': location}).count()
					_way_data.update({'way_id': closest_roads['first_road'], 'location': location}, {'$set': {'n_poi_1': n_poi_11, 'n_poi_2': n_poi_12, 'n_poi_3': n_poi_13}})
		else:
			class_labels.append(1)

		features = [dist1, dist2, n_poi_11, n_poi_21, n_poi_12, n_poi_22, n_poi_13, n_poi_23]
		features = map(float, features)

		training_set.append(features)
		count += 1
		if count==100:
			print count
			count = 0
	# node_list.close()
	client.close()

	return training_set, class_labels


def create_data_set(location):
	client = MongoClient()
	db = client.flickr
	# _way_data = db.way_data
	# _node_data = db.node_data
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

	way_dict = {}
	way_list = _way_data.find({'location': location, 'n_poi_1': {'$exists': True}})
	for way in way_list:
		way_dict[way['way_id']] = way

	node_list = list(_node_data.find({'is_poi': True, 'belongs_to_way': {'$exists': False}, 'closest_roads': {'$exists': True}, 'location': location}))
	print "No of pois to be classified: ", len(node_list)
	data_set = []
	nodes_order = []

	count = 0
	for node in node_list:
		dist1 = dist2 = n_poi_11 = n_poi_21 = n_poi_12 = n_poi_22 = n_poi_13 = n_poi_23 = 0.0
		closest_roads = node.get('closest_roads', None)
		dist1 = closest_roads['first_distance']
		dist2 = closest_roads['second_distance']

		first_road = way_dict.get(closest_roads['first_road'], None)
		if not first_road:
			first_road = _way_data.find_one({'way_id': closest_roads['first_road'], 'location': location})
		if first_road.get('n_poi_1', None):
			n_poi_11 = first_road['n_poi_1']
			n_poi_12 = first_road['n_poi_2']
			n_poi_13 = first_road['n_poi_3']
		else:
			n_poi_11 = _node_data.find({'belongs_to_way': closest_roads['first_road'], 'category': '1', 'location': location}).count()
			n_poi_12 = _node_data.find({'belongs_to_way': closest_roads['first_road'], 'category': '2', 'location': location}).count()
			n_poi_13 = _node_data.find({'belongs_to_way': closest_roads['first_road'], 'category': '3', 'location': location}).count()
			_way_data.update({'way_id': closest_roads['first_road'], 'location': location}, {'$set': {'n_poi_1': n_poi_11, 'n_poi_2': n_poi_12, 'n_poi_3': n_poi_13}})

		second_road = way_dict.get(closest_roads['second_road'], None)
		if not second_road:
			second_road = _way_data.find_one({'way_id': closest_roads['second_road'], 'location': location})
		if second_road.get('n_poi_1', None):
			n_poi_21 = second_road['n_poi_1']
			n_poi_22 = second_road['n_poi_2']
			n_poi_23 = second_road['n_poi_3']
		else:
			n_poi_21 = _node_data.find({'belongs_to_way': closest_roads['second_road'], 'category': '1', 'location': location}).count()
			n_poi_22 = _node_data.find({'belongs_to_way': closest_roads['second_road'], 'category': '2', 'location': location}).count()
			n_poi_23 = _node_data.find({'belongs_to_way': closest_roads['second_road'], 'category': '3', 'location': location}).count()
			_way_data.update({'way_id': closest_roads['second_road'], 'location': location}, {'$set': {'n_poi_1': n_poi_21, 'n_poi_2': n_poi_22, 'n_poi_3': n_poi_23}})
		
		features = [dist1, dist2, n_poi_11, n_poi_21, n_poi_12, n_poi_22, n_poi_13, n_poi_23]
		features = map(float, features)

		nodes_order.append(node['node_id'])
		data_set.append(features)
		count += 1
		if count==500:
			print count
			count = 0
	# node_list.close()
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


def classify(training_set, class_labels, location):

	client = MongoClient()
	db = client.flickr
	# _way_data = db.way_data
	# _node_data = db.node_data
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

	training_set_file_name = 'training_set_file_'+str(location)+'.pkl'
	class_labels_file_name = 'class_labels_file_'+str(location)+'.pkl'
	data_set_file_name = 'data_set_file_'+str(location)+'.pkl'

	training_set_file = open(training_set_file_name, 'wb')
	class_labels_file = open(class_labels_file_name, 'wb')
	data_set_file = open(data_set_file_name, 'wb')

	pickle.dump(training_set, training_set_file, -1)
	pickle.dump(class_labels, class_labels_file, -1)

	classifier = SVC(cache_size=500)
	classifier.fit(training_set, class_labels)

	print "creating data set"
	data_set, nodes_order = create_data_set(location)
	data_set = normalize(data_set)

	pickle.dump(data_set, data_set_file, -1)

	# data_set_file = open('data_set_file.pkl', 'rb')
	# data_set = pickle.load(data_set_file)
	print "Classifying"
	result_labels = classifier.predict(data_set)

	print ''.join(map(str, result_labels))
	print "\n\n"

	for i in xrange(len(result_labels)):
		node = _node_data.find_one({'node_id': nodes_order[i], 'location': location})
		if result_labels[i]==1:
			belongs_to_way = node['closest_roads']['first_road']
		else:
			belongs_to_way = node['closest_roads']['second_road']
			
		_node_data.update({'node_id': nodes_order[i], 'location': location}, {'$set': {'belongs_to_way': belongs_to_way}})

	client.close()
	training_set_file.close()
	class_labels_file.close()
	data_set_file.close()
	


if __name__=='__main__':

	location = 2
	print "creating training set"
	training_set, class_labels = create_training_set(location)
	training_set = normalize(training_set)

	# training_set_file = open('training_set_file_2.pkl', 'rb')
	# class_labels_file = open('class_labels_file_2.pkl', 'rb')
	
	# training_set = pickle.load(training_set_file)
	# class_labels = pickle.load(class_labels_file)

	# training_set_file.close()
	# class_labels_file.close()

	# print len(training_set)
	# print len(class_labels)

	classify(training_set, class_labels, location)