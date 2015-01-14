# Create your views here.
from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from entry.forms import EntryForm
from entry.models import Entries
from journeys.models import Train
from django.db.models import Q

def add_entry(request):
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
            return index(request)
        else:
            # The supplied form contained errors - just print them to the terminal.
            print form.errors
    else:
        # If the request was not a POST, display the form to enter details.
        form = EntryForm()

    # Bad form (or form details), no form supplied...
    # Render the form with error messages (if any).
    return render_to_response('entry/add_entry.html', {'form': form}, context)

def get_train_list(max_results=0, starts_with=''):
	train_list = []
	if starts_with is not "":
		#train_list = Train.objects.filter(train_name__istartswith=starts_with)
		train_list = Train.objects.filter(Q(train_code__istartswith=starts_with) | Q(train_name__istartswith=starts_with)| Q(train_name__contains=starts_with))
	else:
		#train_list = Train.objects.all()
		pass

	if max_results > 0:
		if len(train_list) > max_results:
				train_list = train_list[:max_results]

	#for train in train_list:
	#	train.url = encode_url(train.train_name)

	return train_list

def suggest_trains(request):
	context = RequestContext(request)
	train_list = []
	starts_with = ''
	if request.method == 'GET':
		starts_with = request.GET['suggestion']

	train_list = get_train_list(8, starts_with)

	return render_to_response('entry/train_list.html', {'train_list': train_list }, context)

		
def index(request):
    # Request the context of the request.
    # The context contains information such as the client's machine details, for example.
	context = RequestContext(request)
	journey_list=Entries.objects.all()
	context_dict = {'entries': journey_list}
	return render_to_response('entry/index.html', context_dict, context)