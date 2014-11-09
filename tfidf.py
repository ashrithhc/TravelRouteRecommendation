import mysql.connector
from gensim import corpora, models
import os

def get_tags(conn, cursor):
	try:
		# query = "SELECT photo_id,tags FROM photos,owner WHERE seed_location='1' AND owner.owner_id=photos.owner AND tags!=\"\" AND tourist=1"
		query = "SELECT photo_id,tags FROM sydney"
		# query = "SELECT photo_id,tags FROM paris"
		# query = "SELECT photo_id,tags FROM london"
		# query = "SELECT photo_id,tags FROM singapore"
		# query = "SELECT photo_id,tags FROM newyork"
		# query = "SELECT photo_id,tags FROM sanfrancisco"
		cursor.execute(query)
		rows = cursor.fetchall()
		f = open('tags.txt','w')
		for row in rows:
			if row[1]!="":
				text = str(row[0]) + "|" + row[1].encode('utf-8')
				f.write(text + "\n")
		f.close()
		# cursor.close()
		# conn.close()
	except mysql.connector.Error as err:
		print query
		print(err)
	except Exception as e:
		print(e)

def calc_tfidf():
	class MyCorpus(object):
		def __iter__(self):
			for line in open('tags.txt'):
				yield dictionary.doc2bow(line.split('|')[1].lower().split())
	tags_file = open('tags.txt','r')
	dictionary = corpora.Dictionary(line.split('|')[1].lower().split() for line in tags_file)
	# print dictionary[0]
	print "\n\n"
	corpus_obj = MyCorpus()
	corpus = [vec for vec in corpus_obj]
	tfidf = models.TfidfModel(corpus,normalize=False)
	corpus_tfidf = []
	for doc in tfidf[corpus]:
		corpus_tfidf.append(doc)

	tags_file.close()

	return dictionary,corpus_tfidf
	# for vec in corpus:
	# 	print vec


if __name__=='__main__':
	try:

		mysql_config = {
			'user': 'root',
			'password': 'password',
			'host': '127.0.0.1',
			'database': 'flickr',
		}

		conn = mysql.connector.connect(**mysql_config)
		cursor = conn.cursor()

		# get_tags(conn,cursor)
		# query = "SELECT photo_id,tags FROM sydney"
		# query = "SELECT photo_id,tags FROM paris"
		# query = "SELECT photo_id,tags FROM london"
		# query = "SELECT photo_id,tags FROM singapore"
		# query = "SELECT photo_id,tags FROM newyork"
		query = "SELECT photo_id,tags FROM sanfrancisco"
		cursor.execute(query)
		rows = cursor.fetchall()
		f = open('tags.txt','w')
		for row in rows:
			if row[1]!="":
				text = str(row[0]) + "|" + row[1].encode('utf-8')
				f.write(text + "\n")
		f.close()
		
		dictionary,corpus_tfidf = calc_tfidf()
		# for i in range(len(corpus_tfidf)):
		# 	print "\nDoc: " + str(i+1)
		# 	for item in corpus_tfidf[i]:
		# 		print "\t" + dictionary[item[0]] + ": " + str(item[1])

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
			# query = "UPDATE sydney SET tags=\'" + tags + "\' WHERE photo_id=\'" + photo_id + "\'"
			# query = "UPDATE paris SET tags=\'" + tags + "\' WHERE photo_id=\'" + photo_id + "\'"
			# query = "UPDATE london SET tags=\'" + tags + "\' WHERE photo_id=\'" + photo_id + "\'"
			# query = "UPDATE singapore SET tags=\'" + tags + "\' WHERE photo_id=\'" + photo_id + "\'"
			# query = "UPDATE newyork SET tags=\'" + tags + "\' WHERE photo_id=\'" + photo_id + "\'"
			query = "UPDATE sanfrancisco SET tags=\'" + tags + "\' WHERE photo_id=\'" + photo_id + "\'"
			cursor.execute(query)
			conn.commit()
		tags_file.close()
		conn.close()
		res_file.close()

		# print "\n"
		# i=1
		# for doc in corpus_tfidf:
		# 	print "\nDoc " + str(i) + ":",
		# 	i += 1
		# 	tags = ""
		# 	for item in doc:
		# 		if item[1] > 1.58:
		# 			tags += (dictionary[item[0]] + " ")
		# 	print tags
	except mysql.connector.Error as err:
		print query
		print(err)
	except Exception as e:
		print(e)