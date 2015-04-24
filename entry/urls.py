from django.conf.urls import patterns, url
from entry import views

urlpatterns = patterns('',
    url(r'^train/$', views.train, name='train'),
	url(r'^suggest_trains/$', views.suggest_trains, name='suggest_trains'),
    url(r'^air/$', views.air, name='air'),
	url(r'^populate_source_destinations/$', views.populate_source_destinations, name='populate_source_destinations'),
	)