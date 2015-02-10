from pymongo import MongoClient
import re
from math import log

def get_landmarks(clustersCollection, seed_location):
	clusters = {}
	pattern = "^" + seed_location + ".*"
	regex = re.compile(pattern)
	clustersCursor = clustersCollection.find({"cluster_id":regex})
	for cluster in clustersCursor:
		if cluster["content_score"] >= 8:
			clusters[cluster["cluster_id"]] = cluster["IC_user"]

	return clusters


def rank(seed_location):
	try:
		client = MongoClient()
		db = client.flickr
		clustersCollection = db.clusters
		photosCollection = db.photos

		clusters = get_landmarks(clustersCollection, seed_location)
		popularity = {}

		for cluster in clusters:
			IC_users = clusters[cluster]
			users = IC_users.split(';')
			users.remove("")
			N_user = len(users)

			for i in xrange(len(users)):
				users[i] = users[i].split('=')[0]

			score = float(N_user)
			for user in users:
				n_photos = photosCollection.find({"$and":[{"cluster_info":cluster}, {"owner":user}]}).count()
				score += log(n_photos)

			popularity[cluster] = score

		ranks = sorted(popularity, key=popularity.get, reverse=True)
		for i in xrange(len(ranks)):
			cluster = ranks[i]
			rank = i+1
			clustersCollection.update({"cluster_id":cluster},{"$set":{"rank":rank}})

	except Exception as e:
		print e

if __name__=='__main__':
	rank('1')
	rank('2')
	rank('3')
	rank('4')
	rank('5')
	rank('6')
