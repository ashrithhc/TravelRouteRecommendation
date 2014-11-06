import flickrapi
import xml.etree.ElementTree as ET
import mysql.connector
# import MySQLdb
import json
import sys

api_key = 'c55d1c61df96fedbc444f9fa487e2170'

def tourist_update(rows):

	for row in rows:
		print row[0]

try:

	mysql_config = {
		'user': 'root',
		'password': 'nopassword',
		'host': '127.0.0.1',
		'database': 'flickr',
	}

	conn = mysql.connector.connect(**mysql_config)
	cursor = conn.cursor()

	query = "SELECT * FROM owner where 1"
	cursor.execute(query)
	data = cursor.fetchall()

	tourist_update(data)
			
	conn.close()
	
except mysql.connector.Error as err:
	print query
	print(err)
except Exception as e:
	print(e)
