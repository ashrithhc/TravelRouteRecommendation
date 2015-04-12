from pymongo import MongoClient
import re
import requests
import urllib
import json

def get_reviews():
	client = MongoClient()
	db = client.flickr
	_clusters = db.clusters
	_reviews = db.reviews

	# pattern = "^" + str(location) + ".*$"
	# regex = re.compile(pattern)
	# clusters = _clusters.find({"rank": {"$exists": True}, "cluster_id": regex, "poi_id": {"$ne": None}})
	clusters = _clusters.find({"rank": {"$exists": True}, "poi_id": {"$ne": None}})

	api_key = "AIzaSyDlP4O95tHjiwENoY1t-6kdXZ426Ic6q_8"

	count = 0

	for cluster in clusters:
		name = cluster['address']
		lat = str(cluster['poi_lat'])
		lon = str(cluster['poi_lon'])
		radius = '0.3'

		try:
			name = urllib.quote_plus(name)
		except Exception as e:
			count += 1
			continue
		url = "https://maps.googleapis.com/maps/api/place/textsearch/json?query=%s&key=%s&location=%s,%s&radius=%s" % (name, api_key, lat, lon, radius)

		response = requests.get(url)

		if not response.content:
			continue

		result = json.loads(response.content)

		if not result['status'] == "OK":
			print result['status']
			continue

		place_id = result['results'][0]['place_id']

		url = "https://maps.googleapis.com/maps/api/place/details/json?placeid=%s&key=%s" % (place_id, api_key)

		response = requests.get(url)

		if not response.content:
			continue

		result = json.loads(response.content)

		if not result['status'] == "OK":
			continue

		result = result['result']

		rating = result.get('rating', 0)
		reviews = result.get('reviews', None)

		best_review = None
		best_rating = 0

		if not reviews:
			best_review = "Review not available"

		else:
			for _review in reviews:
				rating = _review.get('rating', 0)
				if rating > best_rating:
					best_rating = rating
					best_review = _review['text']

		best_review = best_review.replace('\n', '')

		review = {
			'cluster_id': cluster['cluster_id'],
			'place_id': place_id,
			'overall_rating': rating,
			'best_rating': best_rating,
			'best_review': best_review
		}

		_reviews.insert(review)

	print count
	client.close()


if __name__=='__main__':
	get_reviews()