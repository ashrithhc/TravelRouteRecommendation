from pymongo import MongoClient
from gensim import corpora, models
import os

def removeNonAscii(s): 
	return "".join(i for i in s if ord(i)<128)

def get_tags(photosCollection, seed_location):
	try:
		photos = photosCollection.find({"$and": [{"seed_location": seed_location}, {"tags": {"$ne": ""}}]},{"photo_id":True, "tags":True})

		f = open('tags.txt','w')
		tags = ""

		for photo in photos:
			tags = removeNonAscii(photo["tags"])
			if tags!="":
				text = photo["photo_id"] + "|" + tags.encode('utf-8')
				f.write(text + "\n")
		f.close()
	except Exception as e:
		print tags
		print(e)

def calc_tfidf():
	class MyCorpus(object):
		def __iter__(self):
			for line in open('tags.txt'):
				yield dictionary.doc2bow(line.split('|')[1].lower().split())
	tags_file = open('tags.txt','r')
	dictionary = corpora.Dictionary(line.split('|')[1].lower().split() for line in tags_file)

	corpus_obj = MyCorpus()
	corpus = [vec for vec in corpus_obj]
	tfidf = models.TfidfModel(corpus,normalize=False)
	corpus_tfidf = []
	for doc in tfidf[corpus]:
		corpus_tfidf.append(doc)

	tags_file.close()

	return dictionary,corpus_tfidf


if __name__=='__main__':
	try:

		client = MongoClient()
		db = client.flickr
		photosCollection = db.photos

		seed_location = 6
		get_tags(photosCollection, seed_location)
		
		dictionary,corpus_tfidf = calc_tfidf()

		tags_file = open('tags.txt','r')
		res_file = open('tags_res.txt','w')
		i=0
		for line in tags_file:
			photo_id = line.split('|')[0]
			tags = ""
			for item in corpus_tfidf[i]:
				if item[1] > 2:
					tags += (dictionary[item[0]].encode('utf-8') + " ")
			if tags!="":
				res_file.write(photo_id+"|"+tags+"\n")
			i+=1

			photosCollection.update({"photo_id":photo_id},{"$set":{"tags":tags}})

		tags_file.close()
		res_file.close()

		client.close()

	except Exception as e:
		print "or here?"
		print(e)