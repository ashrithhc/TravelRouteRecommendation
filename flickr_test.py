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

		ET.dump(root)
		
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
	photos = flickr.photos_search(per_page='500', page='1', lat='28.6100', lon='77.2300', radius='32', extras='tags,geo,date_taken')
	populate_database(photos, conn, cursor, True)

	# for page_no in range(2, no_of_pages+1):
	# 	print "Page number " + str(page_no)
	# 	photos = flickr.photos_search(per_page='500', page=page_no, lat='28.6100', lon='77.2300', radius='32', extras='tags,geo,date_taken')
	# 	populate_database(photos, conn, cursor, False)
			
	conn.close()
	
except mysql.connector.Error as err:
	print query
	print(err)
except Exception as e:
	print(e)
