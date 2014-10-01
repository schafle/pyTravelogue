from django.db import models

# Create your models here.

class Station(models.Model):
	id = models.AutoField(primary_key=True)
	station_name = models.CharField(max_length=128)
	station_code = models.CharField(max_length=128)
	station_lat  = models.FloatField(default=0.0)
	station_long = models.FloatField(default=0.0)
	
	def __unicode__(self):
		#return self.station_code
		return "%s, %s, %s, %s" % (self.station_name, self.station_code, self.station_lat, self.station_long)
	
class Train(models.Model):
    train_name = models.CharField(max_length=250)
    train_code = models.IntegerField(default=0, unique=True)	
    train_source = models.CharField(max_length=128)
    train_destination = models.CharField(max_length=128)
    train_route = models.CharField(max_length=128)

    def __unicode__(self):
        return self.train_code