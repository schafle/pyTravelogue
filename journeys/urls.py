from django.conf.urls import patterns, url
from journeys import views

'''
urlpatterns = patterns('',
        url(r'^$', views.index, name='index'))
'''	
urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^records/$', views.records, name='records'),
    )
	
	