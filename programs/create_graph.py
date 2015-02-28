from itertools import tee, izip, islice
from networkx import DiGraph, shortest_path
from imposm.parser import OSMParser
import sys

nwise = lambda g,n=2: izip(*(islice(g,i,None) for i,g in enumerate(tee(g,n))))

class HighwayCounter(object):
	def __init__(self):
		self.graph = DiGraph()

	def build_graph(self, ways):
		for osmid, tags, refs in ways:
			for segment in nwise(refs):
				weight = 0
				# weight = length(segment)*coef(tags)
				self.graph.add_edge(segment[0], segment[1], weight = weight)


counter = HighwayCounter()
print "Calling parser\n"
p = OSMParser(concurrency=4, ways_callback=counter.build_graph)
p.parse('../osm_data/singapore.osm.bz2')
print len(counter.graph.nodes())
print len(counter.graph.edges())

# shortest_path(graph, source, dest)
