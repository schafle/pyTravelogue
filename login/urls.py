from django.conf.urls import patterns, url
from login import views
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

'''
urlpatterns = patterns('',
        url(r'^$', views.index, name='index'))
'''	
urlpatterns = patterns('',
    #url(r'^$', views.index, name='index'),
    url(r'^register/$', views.register, name='register'),
	url(r'^login/', views.user_login, name='login'),
	url(r'^logout/', views.user_logout, name='logout'),
    url(r'^privacy_policy/', views.privacy_policy),
    url(r'^terms_of_service/', views.terms_of_service),
    )
	
	