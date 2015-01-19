from rtree import index
from pymongo import MongoClient

class Index:

	def __init__(self):
		self.client = MongoClient()
		self.db = self.client.flickr
		self.photos = self.db.photos

	def get_photos(self, location):
		photos = self.photos.find({"$and": [{"seed_location": location}, {"tags": {"$ne": ""}}]})
		return photos

	def create_index(self, location):
		photos = self.get_photos(location)
		# If interleaved=False, the bbox format looks like xmin, xmax, ymin,ymax
		prop = index.Property()
		prop.overwrite = True
		index_file = "index_" + str(location)
		idx = index.Index(index_file, interleaved=False, properties=prop)

		_id = 1
		for photo in photos:
			latitude = float(photo['latitude'])
			longitude = float(photo['longitude'])
			idx.insert(_id, (latitude, latitude, longitude, longitude), obj={
					'photo_id': photo['photo_id'],
					'owner': photo['owner'],
					'latitude': latitude,
					'longitude': longitude
				})
			_id+=1
		idx.close()
		print _id
			

if __name__=='__main__':
	_index = Index()
	# _index.create_index(1)			
	_index.create_index(2)			
	# _index.create_index(3)			
	# _index.create_index(4)			
	# _index.create_index(5)			
	# _index.create_index(6)			

