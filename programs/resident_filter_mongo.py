from math import log
import sys
from pymongo import MongoClient

def entropy_filtering():
	try:

		client = MongoClient()
		db = client.flickr
		ownerCollection = db.owner
		photosCollection = db.photos

		users = ownerCollection.find({}, {'owner_id': True})
		if users.count()==0:
			return

		total_eliminated = 0
		for user in users:
			months = {}
			owner_id = user['owner_id']
			print "\n\n"+owner_id

			dates = photosCollection.find({'owner':owner_id}, {'date_taken':True})
			if dates.count()==0:
				continue

			total = 0
			print "no of photos: ", dates.count()
			for dt in dates:
				dt = dt['date_taken']
				if(dt!='NULL' and int(dt[:4])>=1990):
					mon = dt[:7]
					no_of_images = months.get(mon, 0)
					months[mon] = no_of_images + 1
					total += 1
			entropy = 0
			for mon in months:
				ratio = float(months[mon])/total
				product = ratio*log(ratio)
				entropy -= product
			if entropy > 1.5:
				total_eliminated += total
				ownerCollection.update({'owner_id':owner_id}, {"$set":{"tourist": 0}})

		print "Total photos eliminated: " + str(total_eliminated)
		client.close()


	except Exception as e:
		print(e)
		print sys.exc_traceback.tb_lineno 


entropy_filtering()