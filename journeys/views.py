# Create your views here.
from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from journeys.models import Station
from entry.models import Entries
from django.db.models import Count, Sum, Max, Avg
from django.db import connection
from itertools import *
import re

def index(request):
	# Request the context of the request.
	# The context contains information such as the client's machine details, for example.
	context = RequestContext(request)

	# Query the database for a list of ALL categories currently stored.
	# Order the categories by no. likes in descending order.
	# Retrieve the top 5 only - or all if less than 5.
	# Place the list in our context_dict dictionary which will be passed to the template engine.
	stations_list=Station.objects.all()
	lat_long_list_of_stations=query_to_dicts("select station_name, count(*) as visits, station_lat, station_long from journeys_station join entry_entries where entry_entries.from_station=journeys_station.station_code GROUP BY station_code")
	journey_list=Entries.objects.values('train_name').filter(username=request.user.username).annotate(dcount=Count('train_name'))
	to_station_list=Entries.objects.values('to_station').filter(username=request.user.username).annotate(count_to_stations=Count('to_station'))
	from_station_list=Entries.objects.values('from_station').filter(username=request.user.username).annotate(count_from_stations=Count('from_station'))
	class_selection_list=Entries.objects.values('class_selection').filter(username=request.user.username).annotate(count_class_selection=Count('class_selection'))
	#train_type_list=Entries.objects.values('from_station').annotate(count_from_stations=Count('from_station'))
	berth_list=Entries.objects.values('berth_selection').filter(username=request.user.username).annotate(count_berth=Count('berth_selection'))
	total_distance_travelled=Entries.objects.filter(username=request.user.username).aggregate(Sum('distance_covered'))
	number_of_places=Entries.objects.values('to_station').filter(username=request.user.username).distinct().count()
	name_of_places=Entries.objects.values('to_station').filter(username=request.user.username).distinct()
	number_of_trains=Entries.objects.values('train_name').filter(username=request.user.username).distinct().count()
	number_of_journeys_in_a_year=query_to_dicts("select (select year(date_of_journey)) as year, count(*) as all_from from entry_entries group by (select year(date_of_journey)) order by (select year(date_of_journey))")
	number_of_journeys_in_a_month=query_to_dicts("select (select monthname(date_of_journey)) as months, count(*) as all_from from entry_entries group by (select monthname(date_of_journey)) order by (select month(date_of_journey))")
	number_of_journeys_in_a_weekday=query_to_dicts("select (select dayname(date_of_journey)) as days, count(*) as all_from from entry_entries group by (select dayname(date_of_journey)) order by (select dayofweek(date_of_journey))")
	longest_journey=Entries.objects.filter(username=request.user.username).aggregate(Max('distance_covered'))
	total_number_of_journeys=Entries.objects.filter(username=request.user.username).count()
	average_length_of_journeys=Entries.objects.filter(username=request.user.username).aggregate(Avg('distance_covered'))
	travelogue_rank_distance=1
	train_types_dict_list=train_types(journey_list)
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
	'average_length_of_journeys':int(average_length_of_journeys['distance_covered__avg']),
	'travelogue_rank_distance':travelogue_rank_distance,
	'train_types_dict':train_types_dict_list,
	'lat_long_list_of_stations':lat_long_list_of_stations,
	}

	# Return a rendered response to send to the client.
	# We make use of the shortcut function to make our lives easier.
	# Note that the first parameter is the template we wish to use.
	return render_to_response('journeys/index.html', context_dict, context)

def user(request,user_name_url):
	# Request the context of the request.
	# The context contains information such as the client's machine details, for example.
	context = RequestContext(request)

	current_user=user_name_url
    
	# Query the database for a list of ALL categories currently stored.
	# Order the categories by no. likes in descending order.
	# Retrieve the top 5 only - or all if less than 5.
	# Place the list in our context_dict dictionary which will be passed to the template engine.
	stations_list=Station.objects.all()
	lat_long_list_of_stations=query_to_dicts("select station_name, count(*) as visits, station_lat, station_long from journeys_station join entry_entries where entry_entries.from_station=journeys_station.station_code GROUP BY station_code")
	journey_list=Entries.objects.values('train_name').filter(username=current_user).annotate(dcount=Count('train_name'))
	to_station_list=Entries.objects.values('to_station').filter(username=current_user).annotate(count_to_stations=Count('to_station'))
	from_station_list=Entries.objects.values('from_station').filter(username=current_user).annotate(count_from_stations=Count('from_station'))
	class_selection_list=Entries.objects.values('class_selection').filter(username=current_user).annotate(count_class_selection=Count('class_selection'))
	#train_type_list=Entries.objects.values('from_station').annotate(count_from_stations=Count('from_station'))
	berth_list=Entries.objects.values('berth_selection').filter(username=current_user).annotate(count_berth=Count('berth_selection'))
	total_distance_travelled=Entries.objects.filter(username=current_user).aggregate(Sum('distance_covered'))
	number_of_places=Entries.objects.values('to_station').filter(username=current_user).distinct().count()
	name_of_places=Entries.objects.values('to_station').filter(username=current_user).distinct()
	number_of_trains=Entries.objects.values('train_name').filter(username=current_user).distinct().count()
	number_of_journeys_in_a_year=query_to_dicts("select (select year(date_of_journey)) as year, count(*) as all_from from entry_entries group by (select year(date_of_journey)) order by (select year(date_of_journey))")
	number_of_journeys_in_a_month=query_to_dicts("select (select monthname(date_of_journey)) as months, count(*) as all_from from entry_entries group by (select monthname(date_of_journey)) order by (select month(date_of_journey))")
	number_of_journeys_in_a_weekday=query_to_dicts("select (select dayname(date_of_journey)) as days, count(*) as all_from from entry_entries group by (select dayname(date_of_journey)) order by (select dayofweek(date_of_journey))")
	longest_journey=Entries.objects.filter(username=current_user).aggregate(Max('distance_covered'))
	total_number_of_journeys=Entries.objects.filter(username=current_user).count()
	average_length_of_journeys=Entries.objects.filter(username=request.user.username).aggregate(Avg('distance_covered'))
	travelogue_rank_count=3
	travelogue_rank_distance=1
	train_types_dict_list=train_types(journey_list)
		
	context_dict = {
	'name' : current_user,
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
	'average_length_of_journeys':int(average_length_of_journeys['distance_covered__avg']),
	'travelogue_rank_distance':travelogue_rank_distance,
	'train_types_dict':train_types_dict_list,
	'lat_long_list_of_stations':lat_long_list_of_stations,
	}

	# Return a rendered response to send to the client.
	# We make use of the shortcut function to make our lives easier.
	# Note that the first parameter is the template we wish to use.
	return render_to_response('journeys/user.html', context_dict, context)
	
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
	
def train_types(journey_list):
	'''returns a dictionary with types of trains and their count in journey database'''
	train_types_dict={'Rajdhani':0, 'Duronto':0, 'GaribRath':0, 'Shatabdi':0, 'Express':0}
	train_types_dict_list=[]
	for train in journey_list:
		if re.search('Rajdh', train['train_name']):
			train_types_dict['Rajdhani']+=train['dcount']
		elif re.search('Duronto', train['train_name']):
			train_types_dict['Duronto']+=train['dcount']
		elif re.search('Garib', train['train_name']):
			train_types_dict['GaribRath']+=train['dcount']
		elif re.search('Shat', train['train_name']) and re.search('bdi', train['train_name']):
			train_types_dict['Shatabdi']+=train['dcount']
		else:
			train_types_dict['Express']+=train['dcount']
	for keys, values in train_types_dict.items():
		train_types_dict_list+=[{'train_type':keys, 'count':values}]
	return train_types_dict_list
	
def records(request):
    # Request the context of the request.
    # The context contains information such as the client's machine details, for example.
	context = RequestContext(request)
	journey_list=Entries.objects.all().filter(username=request.user.username).order_by('-date_of_journey')
	context_dict = {'entries': journey_list, 'name' : request.user.username}
	return render_to_response('journeys/records.html', context_dict, context)	