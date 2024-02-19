from django import forms
from .models import Location

class AddressForm(forms.Form):
    region = forms.ModelChoiceField(queryset=Location.objects.filter(level=1), required=False, label='',
                                    empty_label="Выберите регион")
    city = forms.ModelChoiceField(queryset=Location.objects.none(), required=False, label='',
                                  empty_label="Выберите город")
    district = forms.ModelChoiceField(queryset=Location.objects.none(), required=False, label='',
                                      empty_label="Выберите район")
    neighborhood = forms.ModelChoiceField(queryset=Location.objects.none(), required=False, label='',
                                          empty_label="Выберите микрорайон")
    street = forms.ModelChoiceField(queryset=Location.objects.none(), required=False, label='',
                                    empty_label="Выберите улицу")
    building = forms.ModelChoiceField(queryset=Location.objects.none(), required=False, label='',
                                      empty_label="Выберите здание")
