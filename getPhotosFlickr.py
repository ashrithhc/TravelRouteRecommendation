import flickrapi
import xml.etree.ElementTree as ET
import mysql.connector
# import MySQLdb
import json
import sys

api_key = 'c55d1c61df96fedbc444f9fa487e2170'

def populate_database(root, conn, cursor, get_page):
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
			i = 1
			for photo in root.findall('.//photo'):
				photo_attrib = photo.attrib
				photo_id = photo_attrib['id']
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
				seed_location = '2'
				values = (photo_id, lat, lon, owner, place_id, secret, tags, title, date_taken)
				# query = "INSERT IGNORE INTO photos VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, NULL)"
				query = "SELECT * FROM photos where photo_id=%s AND latitude=%s AND longitude=%s AND owner=%s"
				query += " AND place_id=%s AND secret=%s AND tags=%s AND title=%s AND date_taken=%s"
				# query = "SELECT * FROM photos where photo_id='15421415500' AND latitude='28.626437' AND longitude='77.20907' AND owner='44645552@N04' AND place_id='p0DPJshTW7gHTWzyJw' AND secret='cec0ccb69f' AND tags='india temple delhi sikh connaughtplace sikhtemple gurudwarabanglasahib gurudwarabanglasahibtemple' AND title='Gurudwara Bangla Sahib temple' AND date_taken='2014-09-14 05:43:14'"
				# cursor.execute(query)
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
					conn.commit()
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

	mysql_config = {
		'user': 'root',
		'password': 'password',
		'host': '127.0.0.1',
		'database': 'flickr',
	}

	conn = mysql.connector.connect(**mysql_config)
	cursor = conn.cursor()

	flickr = flickrapi.FlickrAPI(api_key)
	print "Page number 1"
	# photos = flickr.photos_search(per_page='500', page='1', lat='28.6100', lon='77.2300', radius='32', extras='tags,geo,date_taken')
	photos = flickr.photos_search(per_page='500', page='1', lat='48.800928', lon='2.345324', radius='32', extras='tags,geo,date_taken')
	no_of_pages = populate_database(photos, conn, cursor, True)

	for page_no in range(2, no_of_pages+1):
		print "Page number " + str(page_no)
		photos = flickr.photos_search(per_page='500', page=page_no, lat='48.800928', lon='2.345324', radius='32', extras='tags,geo,date_taken')
		populate_database(photos, conn, cursor, False)
			
	conn.close()
	
except mysql.connector.Error as err:
	print query
	print(err)
except Exception as e:
	print(e)
