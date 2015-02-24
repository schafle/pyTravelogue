# Create your views here.
from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from journeys.models import Station
from entry.models import Entries
from django.db.models import Count, Sum, Max
from django.db import connection
from itertools import *

def index(request):
	# Request the context of the request.
	# The context contains information such as the client's machine details, for example.
	context = RequestContext(request)

	# Query the database for a list of ALL categories currently stored.
	# Order the categories by no. likes in descending order.
	# Retrieve the top 5 only - or all if less than 5.
	# Place the list in our context_dict dictionary which will be passed to the template engine.
	stations_list=Station.objects.all()
	#journey_list=Entries.objects.annotate(num_trains=Count('train_name')).order_by('-num_trains')[:]
	journey_list=Entries.objects.values('train_name').annotate(dcount=Count('train_name'))
	to_station_list=Entries.objects.values('to_station').annotate(count_to_stations=Count('to_station'))
	from_station_list=Entries.objects.values('from_station').annotate(count_from_stations=Count('from_station'))
	class_selection_list=Entries.objects.values('class_selection').annotate(count_class_selection=Count('class_selection'))
	#train_type_list=Entries.objects.values('from_station').annotate(count_from_stations=Count('from_station'))
	berth_list=Entries.objects.values('berth_selection').annotate(count_berth=Count('berth_selection'))
	total_distance_travelled=Entries.objects.aggregate(Sum('distance_covered'))
	number_of_places=Entries.objects.values('to_station').filter(username=request.user.username).distinct().count()
	number_of_trains=Entries.objects.values('train_name').distinct().count()
	number_of_journeys_in_a_year=query_to_dicts("select (select year(date_of_journey)) as year, count(*) as all_from from entry_entries group by (select year(date_of_journey)) order by (select year(date_of_journey))")
	number_of_journeys_in_a_month=query_to_dicts("select (select monthname(date_of_journey)) as months, count(*) as all_from from entry_entries group by (select monthname(date_of_journey)) order by (select month(date_of_journey))")
	number_of_journeys_in_a_weekday=query_to_dicts("select (select dayname(date_of_journey)) as days, count(*) as all_from from entry_entries group by (select dayname(date_of_journey)) order by (select dayofweek(date_of_journey))")
	longest_journey=Entries.objects.aggregate(Max('distance_covered'))
	total_number_of_journeys=Entries.objects.count()
	travelogue_rank_count=3
	travelogue_rank_distance=1
	
		
	context_dict = {
	'name' : request.user.username,
	'entries':journey_list, 
	'to_stations':to_station_list,
	'from_stations':from_station_list,
	'class_selection':class_selection_list,
	'berths':berth_list, 
	'number_of_places':number_of_places, 
	'number_of_trains':number_of_trains,
	'total_distance_travelled':total_distance_travelled['distance_covered__sum'],
	'number_of_journeys_in_a_year':number_of_journeys_in_a_year,
	'number_of_journeys_in_a_month':number_of_journeys_in_a_month,
	'number_of_journeys_in_a_weekday':number_of_journeys_in_a_weekday,
	'longest_journey':longest_journey['distance_covered__max'],
	'total_number_of_journeys':total_number_of_journeys,
	'travelogue_rank_count':travelogue_rank_count,
	'travelogue_rank_distance':travelogue_rank_distance,
	}

	# Return a rendered response to send to the client.
	# We make use of the shortcut function to make our lives easier.
	# Note that the first parameter is the template we wish to use.
	return render_to_response('journeys/index.html', context_dict, context)
	
def query_to_dicts(query_string):
	"""Run a simple query and produce a generator
	that returns the results as a bunch of dictionaries
	with keys for the column values selected.
	"""
	cursor = connection.cursor()
	cursor.execute(query_string)
	results = cursor.fetchall()
	x = cursor.description
	resultsList = []  
	for r in results:
		i = 0
		d = {}
		while i < len(x):
			d[x[i][0]] = r[i]
			i = i+1
		resultsList.append(d)
	return resultsList
	
def train_types():
	'''returns a dictionary with types of trains and their count in journey database'''
	
def records(request):
    # Request the context of the request.
    # The context contains information such as the client's machine details, for example.
	context = RequestContext(request)
	journey_list=Entries.objects.all().order_by('-date_of_journey')
	context_dict = {'entries': journey_list}
	return render_to_response('journeys/records.html', context_dict, context)	