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
	
	def __unicode__(self):
		#return self.station_code
		return "%s, %s, %s, %s, %s, %s, %s, %s" % (self.train_name, 
			self.date_of_journey, self.from_station, self.to_station, self.class_selection, self.berth_selection, self.comments, self.username)

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
	
	def __unicode__(self):
		#return self.station_code
		return "%s, %s, %s, %s, %s, %s, %s, %s" % (self.ServiceProvider, 
			self.date_of_journey, self.from_airport, self.to_airport, self.class_selection, self.berth_selection, self.comments, self.username)