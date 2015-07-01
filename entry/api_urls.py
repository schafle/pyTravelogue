from django.conf.urls import patterns, url
from entry.api import Api

call_api = Api()
urlpatterns = patterns('',
	url(r'^suggest_trains/(\w+)/(\d+)$', call_api.suggest_trains),
	url(r'^populate_source_destinations/$', call_api.populate_source_destinations),
	)