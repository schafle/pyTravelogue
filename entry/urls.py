from django.conf.urls import patterns, url
from entry import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^add_entry/$', views.add_entry, name='add_entry'), # NEW MAPPING!
	url(r'^suggest_trains/$', views.suggest_trains, name='suggest_trains'),
	)