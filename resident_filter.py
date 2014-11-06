import mysql.connector
from math import log
import sys

def entropy_filtering():
	try:
		mysql_config = {
			'user': 'root',
			'password': 'password',
			'host': '127.0.0.1',
			'database': 'flickr',
		}

		conn = mysql.connector.connect(**mysql_config)
		cursor = conn.cursor()

		query = "SELECT owner_id FROM owner"
		cursor.execute(query)
		users = cursor.fetchall()

		if not users or len(users)==0:
			return

		total_eliminated = 0
		for user in users:
			months = {}
			query = "SELECT date_taken FROM photos WHERE owner = %s"
			cursor.execute(query, (user[0],))
			dates = cursor.fetchall()
			if not dates or len(dates)==0:
				continue
			total = 0
			for dt in dates:
				if(dt!='NULL'):
					_date = dt[0].strftime("%Y-%m-%d %H:%M:%S")
					mon = _date[:7]
					# day = _date[8:10]
					# days = months.get(mon, None)
					# if days is None:
					# 	days = {day:1}
					# else:
					# 	temp = days.get(day, 0)
					# 	days[day] = temp + 1
					no_of_images = months.get(mon, 0)
					months[mon] = no_of_images + 1
					total += 1
			entropy = 0
			for mon in months:
				ratio = float(months[mon])/total
				product = ratio*log(ratio)
				entropy -= product
			if entropy > 1.5:
				# print months
				# print "\n\n"
				total_eliminated += total
				query = "UPDATE owner SET tourist = 0 WHERE owner_id = %s"
				cursor.execute(query, (user[0],))
				conn.commit()

		print "Total photos eliminated: " + str(total_eliminated)




	except mysql.connector.Error as err:
		print(err)
	except Exception as e:
		print(e)
		print sys.exc_traceback.tb_lineno 


entropy_filtering()