__author__ = 'deeksha'

from math import sqrt, pow, radians, cos, sin, asin, sqrt, log, pi


class Bbox:
    def __init__(self):
        # Semi-axes of WGS-84 geoidal reference
        self.WGS84_a = 6378137.0  # Major semiaxis [m]
        self.WGS84_b = 6356752.3  # Minor semiaxis [m]

    # degrees to radians
    def deg2rad(self, degrees):
        return pi*degrees/180.0
    # radians to degrees
    def rad2deg(self, radians):
        return 180.0*radians/pi

    # Earth radius at a given latitude, according to the WGS-84 ellipsoid [m]
    def WGS84EarthRadius(self, lat):
        # http://en.wikipedia.org/wiki/Earth_radius
        An = self.WGS84_a*self.WGS84_a * cos(lat)
        Bn = self.WGS84_b*self.WGS84_b * sin(lat)
        Ad = self.WGS84_a * cos(lat)
        Bd = self.WGS84_b * sin(lat)
        return sqrt( (An*An + Bn*Bn)/(Ad*Ad + Bd*Bd) )

    # Bounding box surrounding the point at given coordinates,
    # assuming local approximation of Earth surface as a sphere
    # of radius given by WGS84
    def boundingBox(self, latitudeInDegrees, longitudeInDegrees, halfSideInKm):
        lat = self.deg2rad(latitudeInDegrees)
        lon = self.deg2rad(longitudeInDegrees)
        halfSide = 1000*halfSideInKm

        # Radius of Earth at given latitude
        radius = self.WGS84EarthRadius(lat)
        # Radius of the parallel at given latitude
        pradius = radius*cos(lat)

        latMin = lat - halfSide/radius
        latMax = lat + halfSide/radius
        lonMin = lon - halfSide/pradius
        lonMax = lon + halfSide/pradius

        return (self.rad2deg(latMin), self.rad2deg(lonMin), self.rad2deg(latMax), self.rad2deg(lonMax))
