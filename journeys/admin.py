from django.contrib import admin
from journeys.models import Station, Train, Airport, Plane
from entry.models import Entries, AirEntries

admin.site.register(Station)
admin.site.register(Train)
admin.site.register(Airport)
admin.site.register(Plane)
admin.site.register(AirEntries)