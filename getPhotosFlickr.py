import flickrapi
import xml.etree.ElementTree as ET
import mysql.connector
import os
import json
import sys

api_key = 'c55d1c61df96fedbc444f9fa487e2170'

def populate_database(root, conn, cursor, get_page, seed_location):
	try:
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
			# i = 1
			for photo in root.findall('.//photo'):
				photo_attrib = photo.attrib
				photo_id = photo_attrib['id']
				lat = photo_attrib['latitude']
				lon = photo_attrib['longitude']
				owner = photo_attrib['owner']
				# place_id = photo_attrib['place_id'] or 'NULL'
				place_id = 'NULL'
				secret = photo_attrib['secret']
				tags = photo_attrib['tags']
				tags = tags.replace("'", "\\'")
				tags = tags.replace("\"", "\\\"")
				title = photo_attrib['title']
				title = title.replace("'", "\\'")
				title = title.replace("\"", "\\\"")
				date_taken = photo_attrib['datetaken']
				values = (photo_id, lat, lon, owner, place_id, secret, tags, title, date_taken, seed_location)
				query = "INSERT IGNORE INTO photos(photo_id,latitude,longitude,owner,place_id,secret,tags,title,date_taken,seed_location)"
				query += " VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
				cursor.execute(query, values)
				query = "INSERT IGNORE INTO owner(owner_id, min_date, max_date) VALUES(%s,%s,%s)"
				cursor.execute(query, (owner, date_taken, date_taken))
				conn.commit()
				query = "UPDATE owner SET min_date=%s where owner_id=%s AND min_date>%s"
				cursor.execute(query, (date_taken, owner, date_taken))
				conn.commit()
				query = "UPDATE owner SET max_date=%s where owner_id=%s AND max_date<%s"
				cursor.execute(query, (date_taken, owner, date_taken))
				conn.commit()


				'''query = "SELECT * FROM photos where photo_id=%s AND latitude=%s AND longitude=%s AND owner=%s"
				query += " AND place_id=%s AND secret=%s AND tags=%s AND title=%s AND date_taken=%s"
				cursor.execute(query, values)
				data = cursor.fetchall()
				if (not data) or len(data)==0:
					values += (seed_location, )
					print str(i)+"  ",
					i += 1
					query = "INSERT INTO photos(photo_id,latitude,longitude,owner,place_id,secret,tags,title,date_taken,seed_location) "
					query += "VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
					cursor.execute(query, values)
					conn.commit()
					query = "INSERT IGNORE INTO owner(owner_id, min_date, max_date) VALUES(%s,%s,%s)"
					cursor.execute(query, (owner, date_taken, date_taken))
					conn.commit()
					query = "UPDATE owner SET min_date=%s where owner_id=%s AND min_date>%s"
					cursor.execute(query, (date_taken, owner, date_taken))
					conn.commit()
					query = "UPDATE owner SET max_date=%s where owner_id=%s AND max_date<%s"
					cursor.execute(query, (date_taken, owner, date_taken))
					conn.commit()'''

			if get_page:
				no_of_pages = int(root[0].attrib['pages'])
				return no_of_pages
			else:
				return -1
		
	except mysql.connector.Error as err:
		print query
		print(err)
	except Exception as e:
		print(e)
		print sys.exc_traceback.tb_lineno 


try:
	os.environ['http_proxy']=''

	mysql_config = {
		'user': 'root',
		'password': 'password',
		'host': '127.0.0.1',
		'database': 'flickr',
	}

	conn = mysql.connector.connect(**mysql_config)
	cursor = conn.cursor()

	flickr = flickrapi.FlickrAPI(api_key)
	print "\nPage number 1"
	#Delhi
	# photos = flickr.photos_search(per_page='500', page='1', lat='28.6100', lon='77.2300', radius='32', extras='tags,geo,date_taken')
	#Sydney (change bbox co-ordinates)
	photos = flickr.photos_search(per_page='500', page='1', bbox='151.115380,-33.946863,151.282921,-33.772384', extras='tags,geo,date_taken')
	#Paris
	# photos = flickr.photos_search(per_page='500', page='1', lat='48.800928', lon='2.345324', radius='32', extras='tags,geo,date_taken')
	#London
	# photos = flickr.photos_search(per_page='500', page='1', bbox='-0.557531,51.264739,0.277430,51.675354', extras='tags,geo,date_taken')
	#Singapore
	# photos = flickr.photos_search(per_page='500', page='1', lat='1.362715', lon='103.802837', radius='32', extras='tags,geo,date_taken')
	#New York
	# photos = flickr.photos_search(per_page='500', page='1', lat='43.376026', lon='-75.669884', radius='32', extras='tags,geo,date_taken')
	# photos = flickr.photos_search(per_page='500', page='1', bbox='-78.833947,42.084892,-73.736291,44.827551', extras='tags,geo,date_taken')
	#San Francisco
	# photos = flickr.photos_search(per_page='500', page='1', bbox='-122.490128,37.722134,-122.416657,37.789994', extras='tags,geo,date_taken')
	# photos = flickr.photos_search(per_page='500', page='1', lat='37.761229', lon='-122.444810', radius='32', extras='tags,geo,date_taken')
	no_of_pages = populate_database(photos, conn, cursor, True, '1')

	for page_no in range(2, no_of_pages+1):
		print "\nPage number " + str(page_no)
		#Delhi
		# photos = flickr.photos_search(per_page='500', page='1', lat='28.38', lon='77.12', radius='32', extras='tags,geo,date_taken')
		#Sydney (change bbox co-ordinates)
		photos = flickr.photos_search(per_page='500', page=page_no, bbox='151.115380,-33.946863,151.282921,-33.772384', extras='tags,geo,date_taken')
		#Paris
		# photos = flickr.photos_search(per_page='500', page=page_no, lat='48.800928', lon='2.345324', radius='32', extras='tags,geo,date_taken')
		#London
		# photos = flickr.photos_search(per_page='500', page=page_no, bbox='-0.557531,51.264739,0.277430,51.675354', extras='tags,geo,date_taken')
		#Singapore
		# photos = flickr.photos_search(per_page='500', page=page_no, lat='1.362715', lon='103.802837', radius='32', extras='tags,geo,date_taken')
		#New York
		# photos = flickr.photos_search(per_page='500', page=page_no, lat='43.376026', lon='-75.669884', radius='32', extras='tags,geo,date_taken')
		# photos = flickr.photos_search(per_page='500', page=page_no, bbox='-78.833947,42.084892,-73.736291,44.827551', extras='tags,geo,date_taken')
		#San Francisco
		# photos = flickr.photos_search(per_page='500', page=page_no, bbox='-122.490128,37.722134,-122.416657,37.789994', extras='tags,geo,date_taken')
		# photos = flickr.photos_search(per_page='500', page=page_no, lat='37.761229', lon='-122.444810', radius='32', extras='tags,geo,date_taken')
		populate_database(photos, conn, cursor, False, '1')
			
	conn.close()
	
except mysql.connector.Error as err:
	print query
	print(err)
except Exception as e:
	print(e)
