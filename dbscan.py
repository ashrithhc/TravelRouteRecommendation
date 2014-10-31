from math import sqrt, pow, radians, cos, sin, asin, sqrt 
import mysql.connector
 
class DBSCAN:  
#Density-Based Spatial Clustering of Application with Noise -> http://en.wikipedia.org/wiki/DBSCAN  
  def __init__(self):  
    self.name = 'DBSCAN'  
    self.DB = [] #Database  
    self.esp = 1 #neighborhood distance for search  
    self.MinPts = 5 #minimum number of points required to form a cluster  
    self.cluster_inx = -1  
    self.cluster = []  
     
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
          print p_tmp.show(), 'is a noise'  
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
        print npoint_tmp.show(), 'is belonged to some cluster'  
 
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
    pointInRegion = []  
    for i in range(len(self.DB)):  
      p_tmp = self.DB[i]  
      if (self.haversine(P, p_tmp) < self.esp and P.lat != p_tmp.lat and P.lon != p_tmp.lon):  
        pointInRegion.append(p_tmp)  
    return pointInRegion  
 
  def dist(self, p1, p2):  
  #return distance between two point  
    dx = (p1.lat - p2.lat)  
    dy = (p1.lon - p2.lon)  
    return sqrt(pow(dx,2) + pow(dy,2))  

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
  def __init__(self,uid = 0, lat = 0, lon = 0, visited = False, isnoise = False):  
    self.id = uid
    self.lat = lat  
    self.lon = lon  
    self.visited = False  
    self.isnoise = False  
 
  def show(self):  
    return self.lat, self.lon  
     
if __name__=='__main__':  
  #this is a mocking data just for test
  # vecPoint = [Point(100,50), Point(11,3), Point(10,4), Point(11,5), Point(12,4), Point(13,5), Point(12,6), Point(6,10), Point(8,10), Point(5,12), Point(7,12)]  
  try:
    mysql_config = {
      'user': 'root',
      'password': 'password',
      'host': '127.0.0.1',
      'database': 'flickr',
    }
    conn = mysql.connector.connect(**mysql_config)
    cursor = conn.cursor()
    query = "SELECT id,latitude,longitude FROM photos ORDER BY latitude,longitude LIMIT 100"
    cursor.execute(query)
    rows = cursor.fetchall()
    locs = []
    for row in rows:
      loc = Location(row[0],float(row[1]),float(row[2]))
      locs.append(loc)
    #Create object
    dbScan = DBSCAN()  
    #Load data into object
    dbScan.DB = locs;  
    #Do clustering  
    dbScan.DBSCAN()  
    #Show result cluster
    print len(dbScan.cluster)
    for i in range(len(dbScan.cluster)):
      print 'Cluster: ', i
      print len(dbScan.cluster[i])
    # for i in range(len(dbScan.cluster)):  
    #   print 'Cluster: ', i  
    #   for j in range(len(dbScan.cluster[i])):  
    #     print dbScan.cluster[i][j].show()
  except mysql.connector.Error as err:
    print query
    print(err)
  except Exception as e:
    print(e)