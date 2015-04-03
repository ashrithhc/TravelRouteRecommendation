from imposm.parser import OSMParser
import sys

class HighwayCounter(object):
    def __init__(self):
    	self.highways = 0
    	self.count = 0

    def ways(self, ways):
        for osmid, tags, refs in ways:         
            self.count += 1

    def nodes(self, nodes):
	    for node_id, tags, lat_lon in nodes:
	    	print node_id
	    	print tags
	    	print lat_lon

counter = HighwayCounter()
print "Calling parser\n"
p = OSMParser(concurrency=4, ways_callback=counter.ways)
p.parse('../osm_data/Sydney.osm.bz2')

print counter.count