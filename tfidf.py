import mysql.connector
from gensim import corpora, models
import os



def get_tags(mysql_config):
	try:
		conn = mysql.connector.connect(**mysql_config)
		cursor = conn.cursor()
		query = "SELECT id,tags FROM photos"
		cursor.execute(query)
		rows = cursor.fetchall()
		f = open('tags.txt','a')
		for row in rows:
			text = str(row[0]) + "|" + row[1].encode('utf-8')
			f.write(text + "\n")
		f.close()
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
	tfidf = models.TfidfModel(corpus)
	corpus_tfidf = tfidf[corpus]
	i=1
	for doc in corpus_tfidf:
		print "\nDoc: " + str(i)
		i += 1
		for item in doc:
			print "\t" + dictionary[item[0]] + ": " + str(item[1])

	# for vec in corpus:
	# 	print vec


if __name__=='__main__':

	mysql_config = {
		'user': 'root',
		'password': 'password',
		'host': '127.0.0.1',
		'database': 'flickr',
	}

	# get_tags(mysql_config)
	calc_tfidf()