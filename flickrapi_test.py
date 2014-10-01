import flickrapi
import xml.etree.ElementTree as ET
import mysql.connector

api_key = 'c55d1c61df96fedbc444f9fa487e2170'

flickr = flickrapi.FlickrAPI(api_key)
photos = flickr.photos_search(per_page='100', lat='28.6100', lon='77.2300', radius='32', extras='tags,geo')
ET.dump(photos)

mysql_config = {
	'user': 'root',
	'password': 'password',
	'host': '127.0.0.1',
	'database': 'flickr',
}

conn = mysql.connector.connect(**mysql_config)
