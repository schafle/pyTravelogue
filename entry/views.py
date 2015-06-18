# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from entry.forms import EntryForm, AirEntryForm
from entry.models import Entries, AirEntries
from journeys.models import Train
from django.db.models import Q
from django.db import connection

import collections
import re

def train(request):
	# Get the context from the request.
	context = RequestContext(request)
	# A HTTP POST?
	if request.method == 'POST':
		form = EntryForm(request.POST)
		# Have we been provided with a valid form?
		if form.is_valid():
			# Save the new category to the database.
			form.save(commit=True)
			# Now call the index() view.
			# The user will be shown the homepage.
			print form.errors
		else:
			# The supplied form contained errors - just print them to the terminal.
			print form.errors	
	else:
		# If the request was not a POST, display the form to enter details.
		form = EntryForm()

	# Bad form (or form details), no form supplied...
	# Render the form with error messages (if any).
	return render_to_response('entry/train.html', {'form': form, 'name' : request.user.username}, context)

def add_entry(request):
	# Get the context from the request.
	context = RequestContext(request)
	# Bad form (or form details), no form supplied...
	# Render the form with error messages (if any).
	return render_to_response('entry/add_entry.html', {'name' : request.user.username}, context)


def air(request):
	# Get the context from the request.
    context = RequestContext(request)

    # A HTTP POST?
    if request.method == 'POST':
        form = AirEntryForm(request.POST)

        # Have we been provided with a valid form?
        if form.is_valid():
            # Save the new category to the database.
            form.save(commit=True)

            # Now call the index() view.
            # The user will be shown the homepage.
            return HttpResponseRedirect('/journeys/')
        else:
            # The supplied form contained errors - just print them to the terminal.
            print form.errors
    else:
        # If the request was not a POST, display the form to enter details.
        form = AirEntryForm()

    # Bad form (or form details), no form supplied...
    # Render the form with error messages (if any).
	return render_to_response('entry/air.html', {'form': form, 'name' : request.user.username}, context)

def get_train_list(max_results=0, starts_with=''):
	train_list = []
	if starts_with is not "":
		#train_list = Train.objects.filter(train_name__istartswith=starts_with)
		train_list = Train.objects.filter(Q(train_name__contains=starts_with) | Q(train_code__istartswith=starts_with) | Q(train_name__istartswith=starts_with))
	else:
		#train_list = Train.objects.all()
		pass

	if max_results > 0:
		if len(train_list) > max_results:
				train_list = train_list[:max_results]

	#for train in train_list:
	#	train.url = encode_url(train.train_name)

	return train_list

def get_source_dest_list(starts_with=''):
	if starts_with != '' and starts_with != ' ':
		starts_with=str(starts_with)
		starts_with = starts_with.replace("%[0-9/]" , " ")
		#print(starts_with)
		source_dest_list=[]
		cursor = connection.cursor()
		cursor.execute("select train_route from journeys_train where train_name='"+starts_with+"'")
		source_dest_list = cursor.fetchall()
		#print(source_dest_list)
		#source_dest_list=Train.objects.filter(Q(train_route=starts_with))
		source_dest_str=str(source_dest_list[0][0])
		source_dest_list=source_dest_str.split(":")
		#print(source_dest_list)
		index=0		
		source_dest_dict=collections.OrderedDict()
		while index < len(source_dest_list):
			source_dest_dict[source_dest_list[index]]=source_dest_list[index+1]
			index+=2
	return source_dest_dict

def suggest_trains(request):
	context = RequestContext(request)
	train_list = []
	starts_with = ''
	if request.method == 'GET':
		starts_with = request.GET['suggestion']

	train_list = get_train_list(8, starts_with)

	return render_to_response('entry/train_list.html', {'train_list': train_list }, context)


def populate_source_destinations(request):
	context = RequestContext(request)
	source_dest_list = []
	starts_with = ''
	if request.method == 'GET':
		starts_with = request.GET['suggestion']

	source_dest_list = get_source_dest_list(starts_with)
	#source_dest_list=create_list_source_and_destinations(source_to_dest)
	return render_to_response('entry/source_dest_list.html', {'source_dest_list': source_dest_list }, context)
	