from django.db import models
import datetime
# Create your models here.

class Entries(models.Model):
	train_name = models.CharField(max_length=200)
	date_of_journey= models.DateField()
	from_station = models.CharField(max_length=4)
	to_station = models.CharField(max_length=4)
	class_selection = models.CharField(max_length=128)
	berth_selection = models.CharField(max_length=128)
	comments = models.CharField(max_length=2000)
	
	def __unicode__(self):
		#return self.station_code
		return "%s, %s, %s, %s, %s, %s, %s" % (self.train_name, 
			self.date_of_journey, self.from_station, self.to_station, self.class_selection, self.berth_selection, self.comments)
