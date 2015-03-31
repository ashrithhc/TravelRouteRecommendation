import requests
import json
import xml.etree.ElementTree as ET

# url = "http://open.mapquestapi.com/geocoding/v1/reverse?key=Fmjtd%7Cluurn96z20%2C7x%3Do5-9w8a5u&location="
# lat = 40.053116
# lon = -76.313603

# url = url + str(lat) + "," + str(lon)

# decode = requests.get(url).json()
# # print json.dumps(decode, indent=4, sort_keys=True)

# country = decode["results"][0]["locations"][0]["adminArea1"].encode()
# state = decode["results"][0]["locations"][0]["adminArea3"].encode()
# county = decode["results"][0]["locations"][0]["adminArea4"].encode()
# city = decode["results"][0]["locations"][0]["adminArea5"].encode()

# postalcode = decode["results"][0]["locations"][0]["postalCode"].encode()
# sideofstreet = decode["results"][0]["locations"][0]["sideOfStreet"].encode()
# street = decode["results"][0]["locations"][0]["street"].encode()

# Address = street + ', ' + sideofstreet + ', ' + city + ', ' + county + ', ' + state + ', ' + country + ', ' + postalcode

# print Address

left = 103.853790628
bottom = 1.28609344161
right = 103.854689172
top = 1.28699175839
url = "http://open.mapquestapi.com/xapi/api/0.6/node[amenity=*][bbox=%s,%s,%s,%s]" % (left,bottom,right,top)

# decode = requests.get(url)

# root = ET.fromstring(decode.content)
xml = """<?xml version='1.0' encoding='UTF-8'?>
<osm version="0.6" generator="Osmosis SNAPSHOT-r26564">
  <node id="1570724384" version="2" timestamp="2012-02-19T12:50:31Z" uid="468895" user="pyramid" changeset="10729587" lat="1.2864298" lon="103.8545028">
    <tag k="name" v="Singapore River Cruise"/>
    <tag k="amenity" v="ferry_terminal"/>
  </node>
  <node id="1764794847" version="1" timestamp="2012-05-25T04:07:52Z" uid="602634" user="matx17" changeset="11695137" lat="1.2864988" lon="103.8541137">
    <tag k="amenity" v="toilets"/>
  </node>
  <node id="3157711955" version="1" timestamp="2014-10-30T10:57:42Z" uid="2340936" user="JoeDuffy90" changeset="26433078" lat="1.2863075" lon="103.8542069">
    <tag k="addr:postcode" v="049213"/>
    <tag k="name" v="OverEasy Bar and Diner"/>
    <tag k="amenity" v="restaurant"/>
    <tag k="addr:street" v="Fullerton Road"/>
    <tag k="addr:city" v="Singapore"/>
    <tag k="addr:housenumber" v="1"/>
  </node>
</osm>"""
root = ET.fromstring(xml)
max_tags = 0
poi = None
poi_tags = None
for element in root.findall('*'):
	name = False
	tags = element.findall('*')
	for tag in tags:
		key_value = tag.attrib
		if key_value['k'] == 'name':
			name = True
	if name and len(tags) > max_tags:
		max_tags = len(tags)
		poi = element
		poi_tags = tags

poi_name = ""
if poi is not None:
	for tag in max_tags:
		key_value = tag.attrib
		if key_value['k'] == 'name':
			poi_name = key_value['v']