# Create your views here.
from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from journeys.models import Station
from entry.models import Entries
from django.db.models import Count
from django.db import connections
	
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
	total_distance_travelled=19729
	number_of_places=Entries.objects.values('to_station').distinct().count()
	number_of_trains=Entries.objects.values('from_station').distinct().count()
	num_of_journeys_in_a_year=Entries.objects.extra(select={'month': connections[Entries.objects.db].ops.date_trunc_sql('month', 'date_of_journey')}).values('month').annotate(dcount=Count('date_of_journey'))
	print(num_of_journeys_in_a_year)
	context_dict = {
	'entries':journey_list, 
	'to_stations':to_station_list,
	'from_stations':from_station_list,
	'class_selection':class_selection_list,
	'berths':berth_list, 
	'number_of_places':number_of_places, 
	'number_of_trains':number_of_trains,
	'total_distance_travelled':total_distance_travelled
	}

	# Return a rendered response to send to the client.
	# We make use of the shortcut function to make our lives easier.
	# Note that the first parameter is the template we wish to use.
	return render_to_response('journeys/index.html', context_dict, context)