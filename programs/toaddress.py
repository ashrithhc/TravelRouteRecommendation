import requests
import json

url = "http://open.mapquestapi.com/geocoding/v1/reverse?key=Fmjtd%7Cluurn96z20%2C7x%3Do5-9w8a5u&location="
lat = 40.053116
lon = -76.313603

url = url + str(lat) + "," + str(lon)

decode = requests.get(url).json()
# print json.dumps(decode, indent=4, sort_keys=True)

country = decode["results"][0]["locations"][0]["adminArea1"].encode()
state = decode["results"][0]["locations"][0]["adminArea3"].encode()
county = decode["results"][0]["locations"][0]["adminArea4"].encode()
city = decode["results"][0]["locations"][0]["adminArea5"].encode()

postalcode = decode["results"][0]["locations"][0]["postalCode"].encode()
sideofstreet = decode["results"][0]["locations"][0]["sideOfStreet"].encode()
street = decode["results"][0]["locations"][0]["street"].encode()

Address = street + ', ' + sideofstreet + ', ' + city + ', ' + county + ', ' + state + ', ' + country + ', ' + postalcode

print Address


