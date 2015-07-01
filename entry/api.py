from django.http import HttpResponse
from django.views.generic import View
from django.template import RequestContext
from journeys.models import Train
from django.db.models import Q

import json


class Api(View):
        
    def suggest_trains(self, request, starts_with, result_limit):
        train_list = []
        train_list = self.get_train_list(result_limit, starts_with)
        return HttpResponse(train_list, content_type="application/json")
    
    
    def populate_source_destinations(request):
        context = RequestContext(request)
        source_dest_list = []
        starts_with = ''
        if request.method == 'GET':
            starts_with = request.GET['suggestion']
    
        source_dest_list = get_source_dest_list(starts_with)
        #source_dest_list=create_list_source_and_destinations(source_to_dest)
        #return render_to_response('entry/source_dest_list.html', {'source_dest_list': source_dest_list }, context)
        return HttpResponse(json.dumps(source_dest_list), content_type="application/json")
    
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
            source_dest = []
            while index < len(source_dest_list):
                source_dest_dict = {}
                source_dest_dict["Station"]=source_dest_list[index]
                source_dest_dict["distance"]=source_dest_list[index+1]
                source_dest.append(source_dest_dict)
                index+=2
        return source_dest

    def get_train_list(self, result_limit=5, starts_with=''):
        train_list = []
        train_list = Train.objects.filter(Q(train_name__icontains=starts_with))[:result_limit]
        
        try:
            jsonData = json.dumps([{"train" : train.train_name} for train in train_list])
            return jsonData
        except Exception, e:
            error = "Exception Thrown %s"%(str(e))
            return error
        

