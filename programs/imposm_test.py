from imposm.parser import OSMParser
import sys

class HighwayCounter(object):
    def __init__(self):
    	self.highways = 0
    	self.count = 0

    def ways(self, ways):
        for osmid, tags, refs in ways:         
            self.count += 1

counter = HighwayCounter()
print "Calling parser\n"
p = OSMParser(concurrency=4, ways_callback=counter.ways)
p.parse('../osm_data/new-york_new-york.osm.bz2')

print counter.count