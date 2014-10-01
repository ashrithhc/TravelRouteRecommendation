import flickrapi
import xml.etree.ElementTree as ET

api_key = 'c55d1c61df96fedbc444f9fa487e2170'

flickr = flickrapi.FlickrAPI(api_key)
photos = flickr.photos_search(per_page='100', lat='28.6100', lon='77.2300', radius='32', extras='tags,geo')
ET.dump(photos)

