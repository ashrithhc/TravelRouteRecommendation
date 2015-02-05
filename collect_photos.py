import flickrapi
from pymongo import MongoClient
import xml.etree.ElementTree as ET
import mysql.connector
import os
import json
import sys

api_key = 'c55d1c61df96fedbc444f9fa487e2170'

def populate_database(root, _photos, _owner, get_page, seed_location):
	try:
		root = photos
		if type(photos) == type(' '):
			root = ET.fromstring(photos)

		status = root.attrib['stat']
		print status
		if(status=='fail'):
			child_error = root[0]
			error_attrib = child_error.attrib
			print "Error Code: " + error_attrib['code']
			print "Error Message: " + error_attrib['msg']
		elif(status=='ok'):
			for photo in root.findall('.//photo'):
				photo_attrib = photo.attrib
				photo_id = photo_attrib['id']
				lat = photo_attrib['latitude']
				lon = photo_attrib['longitude']
				owner = photo_attrib['owner']
				place_id = photo_attrib['place_id'] or 'NULL'
				secret = photo_attrib['secret']
				tags = photo_attrib['tags']
				tags = tags.replace("'", "\\'")
				tags = tags.replace("\"", "\\\"")
				title = photo_attrib['title']
				title = title.replace("'", "\\'")
				title = title.replace("\"", "\\\"")
				date_taken = photo_attrib['datetaken']

				photo_document = {
					"photo_id": photo_id,
					"latitude": lat,
					"longitude": lon,
					"owner": owner,
					"place_id": place_id,
					"secret": secret,
					"tags": tags,
					"title": title,
					"date_taken": date_taken,
					"cluster_info": None,
					"seed_location": seed_location,
					"geo_location": { "type" : "Point", "coordinates" : [ float(lon), float(lat) ] }
				}

				owner_document = {
					"owner_id": owner
				}

				photo_exists = _photos.find({"photo_id": photo_id}).count()
				if not photo_exists==1:
					_photos.insert(photo_document)

				owner_exists = _owner.find({"owner_id": owner}).count()
				if not owner_exists==1:
					_owner.insert(owner_document)

			if get_page:
				no_of_pages = int(root[0].attrib['pages'])
				return no_of_pages
			else:
				return -1
		
	except Exception as e:
		print(e)
		print sys.exc_traceback.tb_lineno 


try:

	client = MongoClient()
	db = client.flickr
	_photos = db.photos
	_owner = db.owner

	flickr = flickrapi.FlickrAPI(api_key)
	print "\nPage number 1"
	#Delhi
	# photos = flickr.photos_search(per_page='500', page='1', lat='28.6100', lon='77.2300', radius='32', extras='tags,geo,date_taken')
	#Sydney (change bbox co-ordinates)
	photos = flickr.photos_search(per_page='500', page='1', bbox='150.611382,-34.084597,151.318627,-33.544914', extras='tags,geo,date_taken')
	#Paris
	# photos = flickr.photos_search(per_page='500', page='1', lat='48.800928', lon='2.345324', radius='32', extras='tags,geo,date_taken')
	# photos = flickr.photos_search(per_page='500', page='1', bbox='2.271014,48.819880,2.401820,48.902096', extras='tags,geo,date_taken')
	#London
	# photos = flickr.photos_search(per_page='500', page='1', bbox='-0.489,51.28,0.236,51.686', extras='tags,geo,date_taken')
	#Singapore
	# photos = flickr.photos_search(per_page='500', page='1', lat='1.362715', lon='103.802837', radius='32', extras='tags,geo,date_taken')
	# photos = flickr.photos_search(per_page='500', page='1', bbox='103.604053,1.228510,104.041447,1.441313', extras='tags,geo,date_taken')
	#New York
	# photos = flickr.photos_search(per_page='500', page='1', lat='43.376026', lon='-75.669884', radius='32', extras='tags,geo,date_taken')
	# photos = flickr.photos_search(per_page='500', page='1', bbox='-74.037742,40.545638,-73.713645,40.918185', extras='tags,geo,date_taken')
	#San Francisco
	# photos = flickr.photos_search(per_page='500', page='1', bbox='-122.564801,37.706789,-122.389363,37.888551', extras='tags,geo,date_taken')
	# photos = flickr.photos_search(per_page='500', page='1', lat='37.761229', lon='-122.444810', radius='32', extras='tags,geo,date_taken')
	# no_of_pages = populate_database(photos, conn, cursor, True, '1')
	no_of_pages = populate_database(photos, _photos, _owner, True, '9')

	for page_no in range(2, no_of_pages+1):
		print "\nPage number " + str(page_no)
		#Delhi
		# photos = flickr.photos_search(per_page='500', page='1', lat='28.38', lon='77.12', radius='32', extras='tags,geo,date_taken')
		#Sydney (change bbox co-ordinates)
		photos = flickr.photos_search(per_page='500', page=page_no, bbox='150.611382,-34.084597,151.318627,-33.544914', extras='tags,geo,date_taken')
		#Paris
		# photos = flickr.photos_search(per_page='500', page=page_no, lat='48.800928', lon='2.345324', radius='32', extras='tags,geo,date_taken')
		# photos = flickr.photos_search(per_page='500', page=page_no, bbox='2.271014,48.819880,2.401820,48.902096', extras='tags,geo,date_taken')
		#London
		# photos = flickr.photos_search(per_page='500', page=page_no, bbox='-0.489,51.28,0.236,51.686', extras='tags,geo,date_taken')
		#Singapore
		# photos = flickr.photos_search(per_page='500', page=page_no, lat='1.362715', lon='103.802837', radius='32', extras='tags,geo,date_taken')
		# photos = flickr.photos_search(per_page='500', page=page_no, bbox='103.604053,1.228510,104.041447,1.441313', extras='tags,geo,date_taken')
		#New York
		# photos = flickr.photos_search(per_page='500', page=page_no, lat='43.376026', lon='-75.669884', radius='32', extras='tags,geo,date_taken')
		# photos = flickr.photos_search(per_page='500', page=page_no, bbox='-74.037742,40.545638,-73.713645,40.918185', extras='tags,geo,date_taken')
		#San Francisco
		# photos = flickr.photos_search(per_page='500', page=page_no, bbox='-122.564801,37.706789,-122.389363,37.888551', extras='tags,geo,date_taken')
		# photos = flickr.photos_search(per_page='500', page=page_no, lat='37.761229', lon='-122.444810', radius='32', extras='tags,geo,date_taken')
		# populate_database(photos, conn, cursor, False, '1')
		populate_database(photos, _photos, _owner, False, '1')
	
	client.close()

except Exception as e:
	print(e)
