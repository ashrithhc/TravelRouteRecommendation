from imposm.parser import OSMParser

# simple class that handles the parsed OSM data.
class HighwayCounter(object):
    highways = 0
    count = 0

    def ways(self, ways):
        # callback method for ways
        for osmid, tags, refs in ways:
            # if 'highway' in tags:
            #   self.highways += 1
            self.count += 1

# instantiate counter and parser and start parsing
counter = HighwayCounter()
print "Calling parser"
p = OSMParser(concurrency=4, ways_callback=counter.ways)
p.parse('new-york_new-york.osm')

# done
print counter.count