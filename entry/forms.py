from django import forms
from entry.models import Entries
from django.forms.fields import DateField, ChoiceField, MultipleChoiceField
from django.forms.widgets import RadioSelect, CheckboxSelectMultiple
from django.forms.extras.widgets import SelectDateWidget

BERTH_CHOICES = ('L', 'M', 'U', 'SL','SU','SM', 'Chair')
COACH_CHOICES = ('1-AC', '2-AC', '3-AC', 'SL', 'CC', '2S', 'Other')
							
class EntryForm(forms.ModelForm):
	train_name = forms.CharField(max_length=128, help_text="Train name.")
	date_of_journey = forms.DateField(help_text="DOJ")
	from_station = forms.CharField(max_length=4, help_text="From")
	to_station = forms.CharField(max_length=4, help_text="To")
	class_selection = forms.CharField(max_length=128, help_text="Class")
	berth_selection = forms.CharField(max_length=128, help_text="Berth")
	comments = forms.CharField(max_length=2000, help_text="Comments")
	
    # An inline class to provide additional information on the form.
	class Meta:
	# Provide an association between the ModelForm and a model
		model = Entries
