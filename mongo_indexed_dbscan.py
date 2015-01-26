from math import sqrt, pow, radians, cos, sin, asin, sqrt, log, pi
import mysql.connector
from pymongo import MongoClient
import sys
import time


class DBSCAN:  
#Density-Based Spatial Clustering of Application with Noise -> http://en.wikipedia.org/wiki/DBSCAN  
  def __init__(self):  
    self.name = 'DBSCAN' 
    self.location = 0 
    self.DB = [] #Database  
    self.esp = 0.1 #neighborhood distance for search  
    self.MinPts = 20 #minimum number of points required to form a cluster  
    self.cluster_inx = -1  
    self.cluster = [] 
    self.hashmap = {}
    self.photos_collection = None 
     
  def DBSCAN(self):  
    for i in range(len(self.DB)):  
      p_tmp = self.DB[i]  
      if (not p_tmp.visited):  
        #for each unvisited point P in dataset  
        p_tmp.visited = True 
        NeighborPts = self.regionQuery(p_tmp) 
        if(len(NeighborPts) < self.MinPts):  
          #that point is a noise  
          p_tmp.isnoise = True  
          # print p_tmp.show(), 'is a noise'  
        else:  
          self.cluster.append([])  
          self.cluster_inx = self.cluster_inx + 1  
          self.expandCluster(p_tmp, NeighborPts)     
     
  def expandCluster(self, P, neighbor_points):  
    self.cluster[self.cluster_inx].append(P)  
    iterator = iter(neighbor_points)  
    while True:  
      try:   
        npoint_tmp = iterator.next()  
      except StopIteration:  
        # StopIteration exception is raised after last element  
        break  
      if (not npoint_tmp.visited):  
        #for each point P' in NeighborPts   
        npoint_tmp.visited = True
        NeighborPts_ = self.regionQuery(npoint_tmp)  
        if (len(NeighborPts_) >= self.MinPts):  
          for j in range(len(NeighborPts_)):  
            neighbor_points.append(NeighborPts_[j])  
      if (not self.checkMembership(npoint_tmp)):  
        #if P' is not yet member of any cluster  
        self.cluster[self.cluster_inx].append(npoint_tmp)  
      else:
        pass  
        # print npoint_tmp.show(), 'is belonged to some cluster'  
 
  def checkMembership(self, P):  
    #will return True if point is belonged to some cluster  
    ismember = False  
    for i in range(len(self.cluster)):  
      for j in range(len(self.cluster[i])):  
        if (P.lat == self.cluster[i][j].lat and P.lon == self.cluster[i][j].lon):  
          ismember = True  
    return ismember  
     
  def regionQuery(self, P):  
  #return all points within P's eps-neighborhood, except itself 
    # pointInRegion1 = []  
    # for i in range(len(self.DB)):  
    #   p_tmp = self.DB[i]  
    #   if (self.haversine(P, p_tmp) < self.esp and P.lat != p_tmp.lat and P.lon != p_tmp.lon):  
    #     pointInRegion1.append(p_tmp)

    pointInRegion = []

    # photos = self.photos_collection.find({"$and": [{"seed_location": city}, {"tags": {"$ne": ""}}]})
    radius = 0.1/6371
    range_points = self.photos_collection.find({"$and": [{"geo_location": {"$geoWithin": {"$centerSphere": [[P.lon,P.lat], radius]}}}, {"tags": {"$ne": ""}}]})

    for photo in range_points:  
      p_tmp = self.hashmap.get(photo['photo_id'], None)
      # if (self.haversine(P, p_tmp) < self.esp and P.lat != p_tmp.lat and P.lon != p_tmp.lon):  
      #   pointInRegion.append(p_tmp) 
      pointInRegion.append(p_tmp) 

    # ct = 0
    # for pt in pointInRegion:
    #   flag = False
    #   for pt1 in pointInRegion1:
    #     if(pt.lat==pt1.lat and pt.lon==pt1.lon):
    #       flag = True
    #   if not flag:
    #     ct+=1
    # if ct > 0:
    #   print "Number of points in bbox query not in range query: ", ct

    return pointInRegion


  def haversine(self, p1, p2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    lat1 = p1.lat
    lon1 = p1.lon
    lat2 = p2.lat
    lon2 = p2.lon
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
 
class Location:  
  def __init__(self,uid = 0,owner = "", lat = 0, lon = 0, visited = False, isnoise = False):  
    self.id = uid
    self.owner = owner
    self.lat = lat  
    self.lon = lon  
    self.visited = False  
    self.isnoise = False  
 
  def show(self):  
    return self.lat, self.lon  
     
if __name__=='__main__':  

  try:
    
    client = MongoClient()
    db = client.flickr
    _photos = db.photos
    _location = db.seed_location

    city = 1

    photos = _photos.find({"$and": [{"seed_location": city}, {"tags": {"$ne": ""}}]})
    location = _location.find({"location_id": city})
    seed_location = location[0]['name']
    print "Location: " + seed_location

    locs = []
    hashmap = {}
    for photo in photos:
      loc = Location(photo['photo_id'], photo['owner'], float(photo['latitude']),float(photo['longitude']))
      hashmap[photo['photo_id']] = loc
      locs.append(loc)

    #Create object
    dbScan = DBSCAN()  
    #Load data into object
    dbScan.DB = locs
    dbScan.photos_collection = _photos
    dbScan.hashmap = hashmap 
    dbScan.location = city
    #Start time of clustering
    start_time = time.time() 
    #Do clustering  
    dbScan.DBSCAN()
    #End time of clustering
    print "Time taken for 2dsphere(mongo) indexed DBSCAN: %s seconds." % (time.time()-start_time)
    #Show result cluster
    print "Number of clusters: %s" %str(len(dbScan.cluster))
    
  except Exception as e:
    print(e)