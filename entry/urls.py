from django.conf.urls import patterns, url
from entry import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
	url(r'^suggest_trains/$', views.suggest_trains, name='suggest_trains'),
	url(r'^populate_source_destinations/$', views.populate_source_destinations, name='populate_source_destinations'),
	)