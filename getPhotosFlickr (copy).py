import flickrapi
import xml.etree.ElementTree as ET
import mysql.connector
# import MySQLdb
import json
import re

api_key = 'c55d1c61df96fedbc444f9fa487e2170'

def populate_database(root):
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
			for photo in root.findall('.//photo'):
				photo_attrib = photo.attrib
				photo_id = photo_attrib['id']
				# lat = float(photo_attrib['latitude'])
				# lon = float(photo_attrib['longitude'])
				lat = photo_attrib['latitude']
				lon = photo_attrib['longitude']
				owner = photo_attrib['owner']
				place_id = photo_attrib['place_id']
				secret = photo_attrib['secret']
				tags = photo_attrib['tags']
				tags = tags.replace("'", "\\'")
				tags = tags.replace("\"", "\\\"")
				title = photo_attrib['title']
				date_taken = photo_attrib['datetaken']
				seed_location = '1'
				# query = "INSERT IGNORE INTO photos VALUES(\'" + photo_id + "\'"
				# query += ", " + lat + ", " + lon + ", \'" + owner + "\', \'" + place_id + "\', \'" + secret + "\', \'" + tags + "\'"
				# query += ", \'" + title + "\', NULL)"
				values = (photo_id, lat, lon, owner, place_id, secret, tags, title, date_taken)
				# query = "INSERT IGNORE INTO photos VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, NULL)"
				query = "SELECT photo_id FROM photos where photo_id=%s, latitude=%s, longitude=%s, owner=%s, place_id=%s, secret=%s,"
				query += "tags=%s, title=%s, date_taken=%s"
				cursor.execute(query, values)
				if not cursor.rowcount:
					values += (seed_location, )
					query = "INSERT INTO photos(photo_id,latitude,longitude,owner,place_id,secret,tags,title,date_taken,seed_location) "
					query += "VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
					
					cursor.execute(query, values)
				conn.commit()
		
	except mysql.connector.Error as err:
		print query
		print(err)
	except Exception as e:
		print(e)


def crawl(flickr, conn, cursor, page_no):
	try:
		print "Page number " + str(page_no)
		photos = flickr.photos_search(per_page='500', page=page_no, lat='28.6100', lon='77.2300', radius='32', extras='tags,geo,date_taken')
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
			for photo in root.findall('.//photo'):
				photo_attrib = photo.attrib
				photo_id = photo_attrib['id']
				# lat = float(photo_attrib['latitude'])
				# lon = float(photo_attrib['longitude'])
				lat = photo_attrib['latitude']
				lon = photo_attrib['longitude']
				owner = photo_attrib['owner']
				place_id = photo_attrib['place_id']
				secret = photo_attrib['secret']
				tags = photo_attrib['tags']
				tags = tags.replace("'", "\\'")
				tags = tags.replace("\"", "\\\"")
				title = photo_attrib['title']
				date_taken = photo_attrib['datetaken']
				seed_location = '1'
				# query = "INSERT IGNORE INTO photos VALUES(\'" + photo_id + "\'"
				# query += ", " + lat + ", " + lon + ", \'" + owner + "\', \'" + place_id + "\', \'" + secret + "\', \'" + tags + "\'"
				# query += ", \'" + title + "\', NULL)"
				values = (photo_id, lat, lon, owner, place_id, secret, tags, title, date_taken)
				# query = "INSERT IGNORE INTO photos VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, NULL)"
				query = "SELECT photo_id FROM photos where photo_id=%s, latitude=%s, longitude=%s, owner=%s, place_id=%s, secret=%s,"
				query += "tags=%s, title=%s, date_taken=%s"
				cursor.execute(query, values)
				if not cursor.rowcount:
					values += (seed_location, )
					query = "INSERT INTO photos(photo_id,latitude,longitude,owner,place_id,secret,tags,title,date_taken,seed_location) "
					query += "VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
					
					cursor.execute(query, values)
				conn.commit()
		
	except mysql.connector.Error as err:
		print query
		print(err)
	except Exception as e:
		print(e)


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
	photos = flickr.photos_search(per_page='500', page='1', lat='28.6100', lon='77.2300', radius='32', extras='tags,geo,date_taken')
	# photos = flickr.photos_search(per_page='100', lat='28.6100', lon='77.2300', radius='32', extras='tags,geo,date_taken', format='kdshfk')
	# print photos
	# ET.dump(photos)
	root = photos
	if type(photos) == type(' '):
		root = ET.fromstring(photos)

	# ET.dump(root)
	status = root.attrib['stat']
	if(status=='fail'):
		child_error = root[0]
		error_attrib = child_error.attrib
		print "Error Code: " + error_attrib['code']
		print "Error Message: " + error_attrib['msg']
	elif(status=='ok'):
		no_of_pages = int(root[0].attrib['pages'])
		print "Page number 1"
		for photo in root.findall('.//photo'):
			photo_attrib = photo.attrib
			photo_id = photo_attrib['id']
			lat = photo_attrib['latitude']
			lon = photo_attrib['longitude']
			owner = photo_attrib['owner']
			place_id = photo_attrib['place_id']
			secret = photo_attrib['secret']
			tags = re.escape(photo_attrib['tags'])
			tags = tags.replace("'", "\\'")
			tags = tags.replace("\"", "\\\"")
			title = photo_attrib['title']
			date_taken = photo_attrib['datetaken']
			# query = "INSERT IGNORE INTO photos VALUES(\'" + photo_id + "\'"
			# query += ", " + lat + ", " + lon + ", \'" + owner + "\', \'" + place_id + "\', \'" + secret + "\', \'" + tags + "\'"
			# query += ", \'" + title + "\', \'" + date_taken + "\', NULL)"
			
			values = (photo_id, lat, lon, owner, place_id, secret, tags, title, date_taken)
			# query = "INSERT IGNORE INTO photos VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, NULL)"
			query = "SELECT photo_id FROM photos where photo_id=%s, latitude=%s, longitude=%s, owner=%s, place_id=%s, secret=%s,"
			query += "tags=%s, title=%s, date_taken=%s"
			cursor.execute(query, values)
			if not cursor.rowcount:
				values += (seed_location, )
				query = "INSERT INTO photos(photo_id,latitude,longitude,owner,place_id,secret,tags,title,date_taken,seed_location) "
				query += "VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
				
				cursor.execute(query, values)
			conn.commit()
			
			# cursor.execute(query)
			# conn.commit()

		for page_no in range(2, no_of_pages+1):
			crawl(flickr, conn, cursor, page_no)

		# query = "SELECT tags from photos where photo_id = \'15421970277\'"
		# cursor.execute(query)
		# for row in cursor:
		# 	print "\n\n" + row[0]

	
	conn.close()
	
except mysql.connector.Error as err:
	print query
	print(err)
except Exception as e:
	print(e)
