from django.conf.urls import patterns, url
from journeys import views

'''
urlpatterns = patterns('',
        url(r'^$', views.index, name='index'))
'''	
urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^records/$', views.records, name='records'),
    url(r'^records/air/(?P<journey_id>\w+)/$', views.air_details, name='air_details'),
    url(r'^records/train/(?P<journey_id>\w+)/$', views.train_details, name='train_details'),
    url(r'^air_travel/$', views.air_travel, name='air_travel'),
    url(r'^(?P<user_name_url>\w+)/$', views.user, name='user'),
    )
	
	