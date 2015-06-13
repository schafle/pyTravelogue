from django import forms
from entry.models import Entries, AirEntries
from django.forms.fields import DateField, ChoiceField, MultipleChoiceField
from django.forms.widgets import RadioSelect, CheckboxSelectMultiple
from django.forms.extras.widgets import SelectDateWidget

BERTH_CHOICES = (('L','Lower'),('M','Middle'),('U','Upper'),('SL','SideLower'),('SM','SideMiddle'),('SU','SideUpper'),('Others','Others'))
COACH_CHOICES = (('1-AC','1-AC'),('2-AC','2-AC'),('3-AC','3-AC'),('SL','Sleeper'),('CC','CarChair'),('Others','Others'))
							
class EntryForm(forms.ModelForm):
	train_name = forms.CharField(max_length=32, help_text="Train name.")
	date_of_journey = forms.DateField(help_text="DOJ")
	from_station = forms.CharField(max_length=4, help_text="From")
	to_station = forms.CharField(max_length=4, help_text="To")
	class_selection = forms.ChoiceField(choices=COACH_CHOICES, widget=forms.RadioSelect(), help_text="Class")
	berth_selection = forms.ChoiceField(choices=BERTH_CHOICES, widget=forms.RadioSelect(), help_text="Berth")
	comments = forms.CharField(max_length=2000, help_text="Comments")
	
    # An inline class to provide additional information on the form.
	class Meta:
	# Provide an association between the ModelForm and a model
		model = Entries

BERTH_CHOICES_AIR =(('Window','Window'),('Aisle','Aisle'),('Middle','Middle'))
CLASS_CHOICES_AIR =(('Economy','Economy'),('Business','Business'))

class AirEntryForm(forms.ModelForm):
	ServiceProvider = forms.CharField(max_length=128, help_text="Service Provider")
	date_of_journey = forms.DateField(help_text="DOJ")
	from_airport = forms.CharField(max_length=4, help_text="From")
	to_airport = forms.CharField(max_length=4, help_text="To")
	class_selection = forms.ChoiceField(choices=CLASS_CHOICES_AIR, widget=forms.RadioSelect(), help_text="Class")
	berth_selection = forms.ChoiceField(choices=BERTH_CHOICES_AIR, widget=forms.RadioSelect(), help_text="Berth")
	comments = forms.CharField(max_length=2000, help_text="Comments")
	
    # An inline class to provide additional information on the form.
	class Meta:
	# Provide an association between the ModelForm and a model
		model = AirEntries

