# -*- coding: utf-8 -*-
import matplotlib.pyplot as plot
import math
from filereader import FileReader

class GeoCoord:
	def __init__(self, ID, latitude, longitude):
		self.ID = ID
		self.latitude = latitude
		self.longitude = longitude
		
	def to_string(self):
		return self.ID + ": (" + str(self.latitude) + "," + str(self.longitude) + ")"
		
    #self + GeoCoord> bearing in radians from self to other
	def bearing_to(self, other):
		x = math.cos(other.latitude) * math.sin(other.longitude-self.longitude)
		y = math.cos(self.latitude)*math.sin(other.latitude) - math.sin(self.latitude)*math.cos(other.latitude)*math.cos(other.longitude-self.longitude)
		return math.atan2(x,y)

	r_earth = 6371000 #radius of earth in meters
    #self + GeoCoord> distance "as the crow flies" in meters from self to other
	def distance_to(self,other):
		p = math.cos(self.latitude) * math.cos(other.latitude)
		a = math.pow((math.sin((other.latitude-self.latitude)/2)), 2) + p*math.pow((math.sin((other.longitude-self.longitude)/2)), 2)
		c = 2*math.atan2(math.sqrt(a), math.sqrt(1-a))
		return self.r_earth*c
	
	#self + GeoCoord > polar coordinate of GPS with self as [0,0]
	def polar_coord_of(self, other):
		return [self.bearing_to(other), self.distance_to(other)]


f = FileReader()
data = f.read_csv("ground_stations.csv")
ground_stations = []
for datum in data:
	g_s = GeoCoord(datum[0], datum[1], datum[2])
	ground_stations.append(g_s)
							
drone = GeoCoord("drone", input("Latitude of drone"), input("Longitude of drone"))
drone = GeoCoord("drone", -90.1234, 90.2345)

#plots given Geo coords on a polar plot
#locus in form (degree, radius)
def plotPolar(ground_stations):
	r = []
	theta = []
	for g_s in ground_stations:
		r.append(drone.distance_to(g_s))
		theta.append(drone.bearing_to(g_s))
	area = 20
	colors = theta
	
	fig = plot.figure()
	ax = fig.add_subplot(111, projection='polar')
	c = ax.scatter(theta, r, c=colors, s=area, cmap='hsv', alpha=0.75)
	plot.show()
	
	
#returns the g_s that the drone is closest to
def findnearest(ground_stations):
	nearest = ground_stations[0]
	for g_s in ground_stations:
		if (drone.distance_to(g_s) < drone.distance_to(nearest)):
			nearest = g_s
	return nearest


for g_s in ground_stations:
	print("Polar coordinate of ", g_s.ID, ": ", drone.polar_coord_of(g_s))
	
plotPolar(ground_stations)

print ("Current drone location: (", drone.latitude, ",", drone.longitude, ")")

for g_s in ground_stations:
	print("Distance from ", g_s.ID, ": ", drone.distance_to(g_s))

print("Nearest station is ", findnearest(ground_stations).to_string())
