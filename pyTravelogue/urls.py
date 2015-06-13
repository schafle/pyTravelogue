from django.conf.urls import patterns, include, url
from journeys import views

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	# Examples:
	# url(r'^$', 'pyTravelogue.views.home', name='home'),
	# url(r'^pyTravelogue/', include('pyTravelogue.foo.urls')),

	# Uncomment the admin/doc line below to enable admin documentation:
	# url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

	# Uncomment the next line to enable the admin:
	url(r'^admin/', include(admin.site.urls)),
	url(r'^$', 'login.views.index'),
	url(r'^journeys/', include('journeys.urls')),
	url(r'^entry/', include('entry.urls')),
	url(r'^login/', include('login.urls')),
	url(r'^user/(?P<user_name_url>\w+)/$', views.user, name='user'),
	url(r'^profile/', 'login.views.profile'),
	#url(r'^$', 'login.views.user_login', name='home'), #make this the home page
	url('', include('social.apps.django_app.urls', namespace='social')),
	url('', include('social.apps.django_app.urls', namespace='auth')),
)
