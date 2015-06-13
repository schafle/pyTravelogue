# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from journeys.models import Station
from entry.models import Entries, AirEntries
from django.db.models import Count, Sum, Max, Avg
from django.db import connection
from itertools import *
from operator import itemgetter
import re
from journeys.models import Train, Airport
from math import radians, cos, sin, asin, sqrt
from django.db import models
import collections


def index(request):
	# Request the context of the request.
	# The context contains information such as the client's machine details, for example.
	context = RequestContext(request)
	
	if request.user.is_authenticated():       
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
		berth_list=Entries.objects.values('berth_selection').filter(username=request.user.username).annotate(count_berth=Count('berth_selection'))
		train_types_dict_list=train_types(journey_list)
		number_of_places=Entries.objects.values('to_station').filter(username=request.user.username).distinct().count()
		name_of_places=Entries.objects.values('to_station').filter(username=request.user.username).distinct()
		number_of_trains=Entries.objects.values('train_name').filter(username=request.user.username).distinct().count()
		number_of_journeys_in_a_year=query_to_dicts("select (select year(date_of_journey)) as year, count(*) as all_from from entry_entries where username='"+request.user.username+"' group by (select year(date_of_journey)) order by (select year(date_of_journey))")

		journeys_by_months_dict_list=[
									{'all_from':0, 'months':'January'},
									{'all_from':0, 'months':'February'},
									{'all_from':0, 'months':'March'},
									{'all_from':0, 'months':'April'},
									{'all_from':0, 'months':'May'},
									{'all_from':0, 'months':'June'},
									{'all_from':0, 'months':'July'},
									{'all_from':0, 'months':'August'},
									{'all_from':0, 'months':'September'},
									{'all_from':0, 'months':'October'},
									{'all_from':0, 'months':'November'},
									{'all_from':0, 'months':'December'},
									]
		number_of_journeys_in_a_month=query_to_dicts("select (select monthname(date_of_journey)) as months, count(*) as all_from from entry_entries where username='"+request.user.username+"' group by (select monthname(date_of_journey)) order by (select month(date_of_journey))")
		for dict in number_of_journeys_in_a_month:
			index=0
			for dict_jnw in journeys_by_months_dict_list:
				if dict['months'] == dict_jnw['months']:
					dict_jnw['all_from'] = dict['all_from']
				index+=1
		
		journeys_by_weekdays_dict_list=[
									{'all_from':0, 'days':'Sunday'},
									{'all_from':0, 'days':'Monday'}, 
									{'all_from':0, 'days':'Tuesday'}, 
									{'all_from':0, 'days':'Wednesday'}, 
									{'all_from':0, 'days':'Thursday'}, 
									{'all_from':0, 'days':'Friday'}, 
									{'all_from':0, 'days':'Saturday'}
								]
		number_of_journeys_in_a_weekday=query_to_dicts("select (select dayname(date_of_journey)) as days, count(*) as all_from from entry_entries where username='"+request.user.username+"' group by (select dayname(date_of_journey)) order by (select dayofweek(date_of_journey))")
		for dict in number_of_journeys_in_a_weekday:
			index=0
			for dict_jnw in journeys_by_weekdays_dict_list:
				if dict['days'] == dict_jnw['days']:
					dict_jnw['all_from'] = dict['all_from']
				index+=1
				
		total_number_of_journeys=Entries.objects.filter(username=request.user.username).count()
		travelogue_rank_distance=1
		total_distance_travelled, longest_journey,average_length_of_journeys = _calculate_distance_covered(request)
		
		context_dict = {
		'name' : request.user.username,
		'entries':journey_list, 
		'to_stations':to_station_list,
		'from_stations':from_station_list,
		'class_selection':class_selection_list,
		'berths':berth_list, 
		'number_of_places':number_of_places, 
		'number_of_trains':number_of_trains,
		'total_distance_travelled':total_distance_travelled, 
		'number_of_journeys_in_a_year':number_of_journeys_in_a_year,
		'number_of_journeys_in_a_month':journeys_by_months_dict_list,
		'number_of_journeys_in_a_weekday':journeys_by_weekdays_dict_list,
		'longest_journey':longest_journey,
		'total_number_of_journeys':total_number_of_journeys,
		'average_length_of_journeys':average_length_of_journeys,
		'travelogue_rank_distance':travelogue_rank_distance,
		'train_types_dict':train_types_dict_list,
		'lat_long_list_of_stations':lat_long_list_of_stations,
		}
		
		'''Filling air travel details'''
		distance_covered_air, longest_journey_air, average_distance_covered_air, total_number_of_journeys_air = _calculate_air_distance_covered(request)
		number_of_places_air=AirEntries.objects.values('to_airport').filter(username=request.user.username).distinct().count()
		serviceProviders=AirEntries.objects.values('ServiceProvider').filter(username=request.user.username).annotate(dcount=Count('ServiceProvider'))
		to_airport_list=AirEntries.objects.values('to_airport').filter(username=request.user.username).annotate(count_to_stations=Count('to_airport'))
		from_airport_list=AirEntries.objects.values('from_airport').filter(username=request.user.username).annotate(count_from_stations=Count('from_airport'))
		class_selection_list_air=AirEntries.objects.values('class_selection').filter(username=request.user.username).annotate(count_class_selection=Count('class_selection'))
		berth_list_air=AirEntries.objects.values('berth_selection').filter(username=request.user.username).annotate(count_berth=Count('berth_selection'))
		number_of_journeys_in_a_year_air=query_to_dicts("select (select year(date_of_journey)) as year, count(*) as all_from from entry_airentries where username='"+request.user.username+"' group by (select year(date_of_journey)) order by (select year(date_of_journey))")
		number_of_journeys_in_a_month_air=query_to_dicts("select (select monthname(date_of_journey)) as months, count(*) as all_from from entry_airentries where username='"+request.user.username+"' group by (select monthname(date_of_journey)) order by (select month(date_of_journey))")
		number_of_journeys_in_a_weekday_air=query_to_dicts("select (select dayname(date_of_journey)) as days, count(*) as all_from from entry_airentries where username='"+request.user.username+"' group by (select dayname(date_of_journey)) order by (select dayofweek(date_of_journey))")
		
		
		context_dict['total_distance_travelled'] = context_dict['total_distance_travelled']+distance_covered_air
		if context_dict['longest_journey'] < longest_journey_air:
			context_dict['longest_journey'] = longest_journey_air
		context_dict['serviceProviders'] = serviceProviders
		context_dict['number_of_copanies']=len(serviceProviders)
		context_dict['number_of_places'] = context_dict['number_of_places'] + number_of_places_air
		context_dict['to_airport_list'] = to_airport_list
		context_dict['from_airport_list'] = from_airport_list
		context_dict['berth_list_air'] = berth_list_air
		context_dict['class_selection_list_air'] = class_selection_list_air
		context_dict['number_of_journeys_in_a_year_air'] = number_of_journeys_in_a_year_air
		
		'''ToDo'''
		'''Monthly stats with addition of plane journeys'''
		'''for dict in number_of_journeys_in_a_month_air:
			if month in number_of_journeys_in_a_month.keys():
				number_of_journeys_in_a_month[month]=number_of_journeys_in_a_month[month]+number_of_journeys_in_a_month_air[month]
		'''
		'''Weekly stats with addition of plane journeys'''
		'''for weekday, count in number_of_journeys_in_a_weekday_air:
			if weekday in number_of_journeys_in_a_weekday.keys():
				number_of_journeys_in_a_weekday[weekday]=number_of_journeys_in_a_weekday[weekday]+number_of_journeys_in_a_weekday_air[weekday]		
		
		context_dict['number_of_journeys_in_a_month'] = number_of_journeys_in_a_month
		context_dict['number_of_journeys_in_a_weekday'] = number_of_journeys_in_a_weekday'''
		# Return a rendered response to send to the client.
		# We make use of the shortcut function to make our lives easier.
		# Note that the first parameter is the template we wish to use.
		#print( str(context_dict))
		return render_to_response('journeys/index.html', context_dict, context)
	else:
		return HttpResponseRedirect('/login/login')
	
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
	berth_list=Entries.objects.values('berth_selection').filter(username=current_user).annotate(count_berth=Count('berth_selection'))
	number_of_places=Entries.objects.values('to_station').filter(username=current_user).distinct().count()
	name_of_places=Entries.objects.values('to_station').filter(username=current_user).distinct()
	number_of_trains=Entries.objects.values('train_name').filter(username=current_user).distinct().count()
	number_of_journeys_in_a_year=query_to_dicts("select (select year(date_of_journey)) as year, count(*) as all_from from entry_entries where username='"+request.user.username+"' group by (select year(date_of_journey)) order by (select year(date_of_journey))")
	number_of_journeys_in_a_month=query_to_dicts("select (select monthname(date_of_journey)) as months, count(*) as all_from from entry_entries where username='"+request.user.username+"' group by (select monthname(date_of_journey)) order by (select month(date_of_journey))")
	number_of_journeys_in_a_weekday=query_to_dicts("select (select dayname(date_of_journey)) as days, count(*) as all_from from entry_entries where username='"+request.user.username+"'group by (select dayname(date_of_journey)) order by (select dayofweek(date_of_journey))")
	total_number_of_journeys=Entries.objects.filter(username=current_user).count()
	total_distance_travelled, longest_journey,average_length_of_journeys = _calculate_distance_covered(request)
	
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
	'total_distance_travelled':total_distance_travelled,
	'number_of_journeys_in_a_year':number_of_journeys_in_a_year,
	'number_of_journeys_in_a_month':number_of_journeys_in_a_month,
	'number_of_journeys_in_a_weekday':number_of_journeys_in_a_weekday,
	'longest_journey':longest_journey,
	'total_number_of_journeys':total_number_of_journeys,
	'average_length_of_journeys':average_length_of_journeys,
	'travelogue_rank_distance':travelogue_rank_distance,
	'train_types_dict':train_types_dict_list,
	'lat_long_list_of_stations':lat_long_list_of_stations,
	}

	# Return a rendered response to send to the client.
	# We make use of the shortcut function to make our lives easier.
	# Note that the first parameter is the template we wish to use.
	return render_to_response('journeys/user.html', context_dict, context)

def air_travel(request):
	# Request the context of the request.
	# The context contains information such as the client's machine details, for example.
	context = RequestContext(request)
	
	if request.user.is_authenticated():       
		# Query the database for a list of ALL categories currently stored.
		# Order the categories by no. likes in descending order.
		# Retrieve the top 5 only - or all if less than 5.
		# Place the list in our context_dict dictionary which will be passed to the template engine.
		distance_covered, longest_journey, average_distance_covered, total_number_of_journeys = _calculate_air_distance_covered(request)
		number_of_places=AirEntries.objects.values('to_airport').filter(username=request.user.username).distinct().count()
		serviceProviders=AirEntries.objects.values('ServiceProvider').filter(username=request.user.username).annotate(dcount=Count('ServiceProvider'))
		to_airport_list=AirEntries.objects.values('to_airport').filter(username=request.user.username).annotate(count_to_stations=Count('to_airport'))
		from_airport_list=AirEntries.objects.values('from_airport').filter(username=request.user.username).annotate(count_from_stations=Count('from_airport'))
		class_selection_list=AirEntries.objects.values('class_selection').filter(username=request.user.username).annotate(count_class_selection=Count('class_selection'))
		berth_list=AirEntries.objects.values('berth_selection').filter(username=request.user.username).annotate(count_berth=Count('berth_selection'))
		number_of_journeys_in_a_year=query_to_dicts("select (select year(date_of_journey)) as year, count(*) as all_from from entry_airentries where username='"+request.user.username+"' group by (select year(date_of_journey)) order by (select year(date_of_journey))")
		number_of_journeys_in_a_month=query_to_dicts("select (select monthname(date_of_journey)) as months, count(*) as all_from from entry_airentries where username='"+request.user.username+"' group by (select monthname(date_of_journey)) order by (select month(date_of_journey))")
		number_of_journeys_in_a_weekday=query_to_dicts("select (select dayname(date_of_journey)) as days, count(*) as all_from from entry_airentries where username='"+request.user.username+"' group by (select dayname(date_of_journey)) order by (select dayofweek(date_of_journey))")
	
		context_dict = {
						'total_distance_travelled':distance_covered,
						'longest_journey':longest_journey,
						'average_distance_covered':average_distance_covered,
						'number_of_places':number_of_places,
						'serviceProviders':serviceProviders,
						'number_of_copanies':len(serviceProviders),
						'travelogue_rank_distance':1,
						'to_airport_list':to_airport_list,
						'from_airport_list':from_airport_list,
						'berths':berth_list, 
						'number_of_places':number_of_places,
						'class_selection':class_selection_list,
						'total_number_of_journeys':total_number_of_journeys,
						'number_of_journeys_in_a_year':number_of_journeys_in_a_year,
						'number_of_journeys_in_a_month':number_of_journeys_in_a_month,
						'number_of_journeys_in_a_weekday':number_of_journeys_in_a_weekday,
						'name':request.user.username,
						}
	return render_to_response('journeys/air_travel.html', context_dict, context)


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
	journey_list=Entries.objects.values('id', 'train_name','from_station','to_station','comments','date_of_journey').filter(username=request.user.username).order_by('-date_of_journey')
	journey_list_air=AirEntries.objects.values('id', 'ServiceProvider','from_airport','to_airport','comments','date_of_journey').filter(username=request.user.username).order_by('-date_of_journey')
	result_list = sorted(chain(journey_list, journey_list_air), key=itemgetter('date_of_journey'), reverse=True)
	context_dict = {'entries': result_list,'name' : request.user.username}
	return render_to_response('journeys/records.html', context_dict, context)

def air_details(request, journey_id):
	# Request the context of the request.
    # The context contains information such as the client's machine details, for example.
	context = RequestContext(request)
	journey_list=AirEntries.objects.values('id', 'ServiceProvider','from_airport','to_airport','comments','date_of_journey').filter(username=request.user.username, id=journey_id).order_by('-date_of_journey')
	distance_covered = calculate_point_to_point_distance(journey_list[0]['from_airport'], journey_list[0]['to_airport'])
	lat_long_list = Airport.objects.values('station_code', 'station_lat', 'station_long').filter(models.Q(station_code=journey_list[0]['from_airport']) | models.Q(station_code=journey_list[0]['to_airport']))
	if lat_long_list[0]['station_code']==journey_list[0]['from_airport']:
		source = lat_long_list[0]
		destination = lat_long_list[1]
	else: 
		source = lat_long_list[1]
		destination = lat_long_list[0]
		
	context_dict = {'entries': journey_list[0], 
					'route_from':source,
					'route_to':destination,
					'comments':journey_list[0]['comments'],
					'distance_covered': int(distance_covered),
					'name' : request.user.username}
	return render_to_response('journeys/air_details.html', context_dict, context)
	

def train_details(request, journey_id):
	# Request the context of the request.
    # The context contains information such as the client's machine details, for example.
	context = RequestContext(request)
	journey_list=Entries.objects.values('id', 'train_name','from_station','to_station','comments','date_of_journey').filter(username=request.user.username, id=journey_id).order_by('-date_of_journey')
	route = get_train_route(journey_list[0]['train_name'], journey_list[0]['from_station'], journey_list[0]['to_station'])
	distance_covered = train_distance_covered(journey_list[0]['train_name'], journey_list[0]['from_station'], journey_list[0]['to_station'])
	context_dict = {'entries': journey_list[0], 
					'route':route, 
					'comments':journey_list[0]['comments'],
					'distance_covered':distance_covered,
					'name' : request.user.username}
	return render_to_response('journeys/train_details.html', context_dict, context)

def get_train_route(train, _from, _to):
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
		route_list = route_list[0::2]
		route_list = route_list[route_list.index(_from):route_list.index(_to)+1]
		route_dict = collections.OrderedDict()
		for place in route_list:
			route_dict[place] = Station.objects.values('station_lat', 'station_long').filter(station_code=place)
	except Exception, e:
		print("Something went wrong %s" % e)
		return 0
	return route_dict

def train_distance_covered(train, from_station, to_station):
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
		distance_covered = 	int(route_dict[to_station]) - int(route_dict[from_station])
	except Exception, e:
		print("Something went wrong %s" % e)
		return 0
	return distance_covered
	
def _calculate_distance_covered(request):
	'''Returns the total distance travelled '''
	journey_list=Entries.objects.values('train_name', 'from_station', 'to_station').filter(username=request.user.username)
	total_distance_covered = 0
	maximum_distance_covered = 0
	for journey in journey_list:
		train = journey['train_name']
		_from = journey['from_station']
		_to = journey['to_station']
		distance_covered_in_this_journey = train_distance_covered(train, _from, _to)
		total_distance_covered += distance_covered_in_this_journey
		if maximum_distance_covered < distance_covered_in_this_journey:
			maximum_distance_covered = distance_covered_in_this_journey
		
	average_length_of_journey = total_distance_covered/len(journey_list)
	return (total_distance_covered, maximum_distance_covered, average_length_of_journey)

def _calculate_air_distance_covered(request):
	"""
	Calculate the great circle distance between two points 
	on the earth (specified in decimal degrees)
	"""
	distance_covered = 0
	longest_journey = 0
	journey_list=AirEntries.objects.values('from_airport', 'to_airport').filter(username=request.user.username)
	
	for journey in journey_list:
		_from = journey['from_airport']
		_to = journey['to_airport']
		distance_covered_in_this_trip = calculate_point_to_point_distance(_from, _to) 
		if longest_journey < distance_covered_in_this_trip:
			longest_journey = distance_covered_in_this_trip
		distance_covered += distance_covered_in_this_trip
		
	average_distance_covered = distance_covered/len(journey_list)
	return (int(distance_covered), int(longest_journey), int(average_distance_covered), len(journey_list))

def calculate_point_to_point_distance(_from, _to):
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
		print("Exception Thrown ==> "+str(e)) 
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
