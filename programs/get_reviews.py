from pymongo import MongoClient
import requests
import urllib
import json
from PIL import Image
import urllib2

def get_reviews():
	client = MongoClient()
	db = client.flickr
	_clusters = db.clusters
	_reviews = db.reviews

	clusters = _clusters.find({"rank": {"$exists": True}, "poi_id": {"$ne": None}})

	api_key = "AIzaSyDEUFu6OkgmpVMW5-MHOEqA-xPF9_R-XMU"

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

		photo_reference = None

		if result.get('photos', None):
			photo_reference = result['photos'][0]['photo_reference']

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
			'best_review': best_review,
			'photo_reference': photo_reference
		}

		_reviews.insert(review)

	print count
	client.close()


def get_photos():
	client = MongoClient()
	db = client.flickr
	_reviews = db.reviews

	l = ['11','17','18','21','25','26','27','31','33','35','37','58','59','62','64','68','69','110','111','212','221','310','312','313','314','322','331','333','339','511','513','514','614','615','616','620','623','629','630','632','640']

	for i in l:
		_reviews.update({'cluster_id': i},{'$set': {'photo_exists': True}})

	# reviews = _reviews.find({'photo_reference': {'$ne': None}})

	# api_key = "AIzaSyB2haQDsHSXSQD6H3YArvO89QIZ3BzgRSo"

	# for review in reviews:
	# 	photo_reference = review['photo_reference']
	# 	cluster_id = review['cluster_id']
	# 	url = "https://maps.googleapis.com/maps/api/place/photo?maxwidth=1600&photoreference=%s&key=%s" % (photo_reference, api_key)
	# 	try:
	# 		opener1 = urllib2.build_opener()
	# 		result = opener1.open(url)
	# 		image = result.read()
	# 		filename = "../TravelRouteRecommendation/route_recommendation/static/places/" + cluster_id + ".jpg"
	# 		fout = open(filename, "wb")
	# 		fout.write(image)
	# 		fout.close()
	# 	except Exception as e:
	# 		continue

	client.close()


if __name__=='__main__':
	# get_reviews()
	get_photos()