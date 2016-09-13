# -*- coding: utf-8 -*-
"""
Created on Sun Aug 14 23:49:53 2016

@author: Kimberly
"""

from django import forms
from datetime import datetime

class ReportSettingsForm(forms.Form):
    select = forms.CharField(max_length=100)
    
#    date_start = forms.DateField()
#    date_end = forms.DateField()

class NameForm(forms.Form):
    #your_name = forms.CharField(label='Your name', max_length=100)
                                            #(value, key)
    something = forms.ChoiceField(choices = [('Bonia Indonesia','Bonia Indonesia'), ('www.thebodyshop.com.my','www.thebodyshop.com.my')], label="", initial='', widget=forms.Select(), required=True)
    
class DateForm(forms.Form):    
    n_start = forms.DateField(initial=datetime.now().date())
    n_end = forms.DateField(initial=datetime.now().date())
    p_start = forms.DateField(initial=datetime.now().date())
    p_end = forms.DateField(initial=datetime.now().date())

class TypeForm(forms.Form):
    rep_type = forms.ChoiceField(choices = [('ga','Google Analytics'), ('ad','Adwords'), ('fb', 'Facebook')], label="", initial='', widget=forms.RadioSelect(), required=True)  