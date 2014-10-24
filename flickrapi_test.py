import flickrapi
import xml.etree.ElementTree as ET
import mysql.connector
import json

api_key = 'c55d1c61df96fedbc444f9fa487e2170'

try:

	mysql_config = {
		'user': 'root',
		'password': 'password',
		'host': '127.0.0.1',
		'database': 'flickr',
	}

	conn = mysql.connector.connect(**mysql_config)
	cursor = conn.cursor()

	flickr = flickrapi.FlickrAPI(api_key)
	photos = flickr.photos_search(per_page='5', lat='28.6100', lon='77.2300', radius='32', extras='tags,geo')
	# photos = flickr.photos_search(per_page='100', lat='28.6100', lon='77.2300', radius='32', extras='tags,geo', format='kdshfk')
	# print photos
	# ET.dump(photos)
	root = photos
	if type(photos) == type(' '):
		root = ET.fromstring(photos)

	status = root.attrib['stat']
	if(status=='fail'):
		child_error = root[0]
		error_attrib = child_error.attrib
		print "Error Code: " + error_attrib['code']
		print "Error Message: " + error_attrib['msg']
	elif(status=='ok'):
		no_of_pages = int(root[0].attrib['pages'])
		# print(no_of_pages)
		for photo in root.findall('.//photo'):
			photo_attrib = photo.attrib
			photo_id = photo_attrib['id']
			lat = photo_attrib['latitude']
			lon = photo_attrib['longitude']
			owner = photo_attrib['owner']
			place_id = photo_attrib['place_id']
			secret = photo_attrib['secret']
			tags = photo_attrib['tags']
			title = photo_attrib['title']
			query = "INSERT IGNORE INTO photos VALUES(\'" + photo_id + "\'"
			query += ", " + lat + ", " + lon + ", \'" + owner + "\', \'" + place_id + "\', \'" + secret + "\', \'" + tags + "\'"
			query += ", \'" + title + "\', NULL)"
			cursor.execute(query)
			conn.commit()

		# query = "SELECT tags from photos where photo_id = \'15421970277\'"
		# cursor.execute(query)
		# for row in cursor:
		# 	print "\n\n" + row[0]

	
	conn.close()
	
except mysql.connector.Error as err:
	print(err)
except Exception as e:
	print(e)
