from math import sqrt, pow, radians, cos, sin, asin, sqrt, log

class Haversine:
    def __init__(self):
        pass

    def get_distance(self, point1, point2):
        """
        Calculate the great circle distance between two points 
        on the earth (specified in decimal degrees)
        """
        lat1 = point1['latitude']
        lon1 = point1['longitude']
        lat2 = point2['latitude']
        lon2 = point2['longitude']
        
        # convert decimal degrees to radians 
        lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

        # haversine formula 
        dlon = lon2 - lon1 
        dlat = lat2 - lat1 
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * asin(sqrt(a)) 

        # 6367 km is the radius of the Earth
        km = 6367 * c
        return km
