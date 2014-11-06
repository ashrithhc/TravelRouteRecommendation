import flickrapi
from elementtree.ElementTree import Element, SubElement, dump

api_key = '0f45b1c4923e3462403afa9f542a14f2'

flickr = flickrapi.FlickrAPI(api_key)

photos = flickr.photos_search(per_page='500', lat='28.38', lon='77.12', radius='32', extras='geo,tags')
dump(photos)
