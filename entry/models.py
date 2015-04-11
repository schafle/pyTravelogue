from math import radians, cos, sin, asin, sqrt
from django.db import models
import datetime
from journeys.models import Train, Airport
# Create your models here.

class Entries(models.Model):
	id = models.AutoField(primary_key=True)
	berth_choices =(('L','Lower'),('M','Middle'),('U','Upper'),('SL','SideLower'),('SM','SideMiddle'),('SU','SideUpper'),('Others','Others'))
	class_choices =(('1-AC','1-AC'),('2-AC','2-AC'),('3-AC','3-AC'),('SL','Sleeper'),('CC','CarChair'),('Others','Others'))
	train_name = models.CharField(max_length=200)
	date_of_journey= models.DateField()
	from_station = models.CharField(max_length=4)
	to_station = models.CharField(max_length=4)
	class_selection = models.CharField(max_length=6, choices=class_choices)
	berth_selection = models.CharField(max_length=6, choices=berth_choices)
	comments = models.CharField(max_length=2000)
	username = models.CharField(max_length=30)
	
	def _calculate_distance_covered(self):
		'''Returns the total distance travelled '''
		train = self.train_name
		_from = self.from_station
		_to = self.to_station
		try:
			train_route = Train.objects.values('train_route').filter(train_name=train)
			if len(train_route) > 1:
				print(" There are more than one trains with this train name. Something wrong with database")
				return 0
		except Exception, e:
			print("Exception Thrown"+str(e))
			return 0
		try:
			route_list = train_route[0]['train_route'].split(":")
			route_dict = dict(zip(route_list[::2], route_list[1::2]))
			distance_covered = 	int(route_dict[_to]) - int(route_dict[_from])
		except Exception, e:
			print("Something went wrong %s" % e)
			return 0
		return distance_covered
	distance_covered = property(_calculate_distance_covered)
	
	def __unicode__(self):
		#return self.station_code
		return "%s, %s, %s, %s, %s, %s, %s, %s, %d" % (self.train_name, 
			self.date_of_journey, self.from_station, self.to_station, self.class_selection, self.berth_selection, self.comments, self.username, self.distance_covered)
	
	

class AirEntries(models.Model):
	id = models.AutoField(primary_key=True)
	berth_choices =(('Window','Window'),('Aisle','Aisle'),('Middle','Middle'))
	class_choices =(('Economy','Economy'),('Business','Business'))
	ServiceProvider = models.CharField(max_length=200)
	date_of_journey= models.DateField()
	from_airport = models.CharField(max_length=3)
	to_airport = models.CharField(max_length=3)
	class_selection = models.CharField(max_length=10, choices=class_choices)
	berth_selection = models.CharField(max_length=10, choices=berth_choices)
	comments = models.CharField(max_length=2000)
	username = models.CharField(max_length=30)
	#distance_covered = distance_covered_calc(from_airport, to_airport)
	
	def _calculate_air_distance_covered(self):
		"""
		Calculate the great circle distance between two points 
		on the earth (specified in decimal degrees)
		"""
		_from = self.from_airport
		_to = self.to_airport
		try:
			lat_long_list = Airport.objects.values('station_code', 'station_lat', 'station_long').filter(models.Q(station_code=_to) | models.Q(station_code=_from))
			if len(lat_long_list) > 2:
				print("Something went wrong. Database needs to be checked for data with same aiport code")
				return 0
			lon1 = lat_long_list[0]['station_long']
			lat1 = lat_long_list[0]['station_lat']
			lon2 = lat_long_list[1]['station_long']
			lat2 = lat_long_list[1]['station_lat']
			
		except Exception, e:
			print("Exception Thrown"+str(e)) 
			return 0
		
		# convert decimal degrees to radians 
		lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
	
		# haversine formula 
		dlon = lon2 - lon1 
		dlat = lat2 - lat1 
		a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
		c = 2 * asin(sqrt(a)) 
		r = 6371 # Radius of earth in kilometers. Use 3956 for miles
		return c * r

	distance_covered = property(_calculate_air_distance_covered)
	
	def __unicode__(self):
		#return self.station_code
		return "%s, %s, %s, %s, %s, %s, %s, %s, %d" % (self.ServiceProvider, 
			self.date_of_journey, self.from_airport, self.to_airport, self.class_selection, self.berth_selection, self.comments, self.username, self.distance_covered)

