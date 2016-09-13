from django.shortcuts import render
from django.http import HttpResponse
from .forms import NameForm, DateForm, TypeForm
import ga_nosampling_example_test1
import os
from dashboard.models import GA_Data
# Create your views here.

def something(d_start, d_end, p_start, p_end, profile):
    current = GA_Data.objects.filter(date_start__exact=d_start).filter(date_end__exact=d_end).filter(profile__exact=profile).get() 
    previous = GA_Data.objects.filter(date_start__exact=p_start).filter(date_end__exact=p_end).filter(profile__exact=profile).get() 
    perc_pv = round((((current.pageview/(current.pageview+previous.pageview)) * 100)-((previous.pageview/(current.pageview+previous.pageview)) * 100)),2)
    perc_bounce = round((((current.bouncerate/(current.bouncerate+previous.bouncerate)) * 100)-((previous.bouncerate/(current.bouncerate+previous.bouncerate)) * 100)), 2)
    perc_trans = round((((current.transactions/(current.transactions+previous.transactions)) * 100)-((previous.transactions/(current.transactions+previous.transactions)) * 100)), 2)
    
    report ={}
    report['Dates'] = [d_start+ ' to ' +d_end, p_start+ ' to ' +p_end, 'Percentage']
    report['Pageview'] = [current.pageview, previous.pageview, perc_pv]
    report['Bouncerate'] = [current.bouncerate, previous.bouncerate, perc_bounce]
    report['Transaction'] = [current.transactions, previous.transactions, perc_trans]
    return report


def index(request):
    return render(request, 'dashboard/index.html')
  
def embed_api(request):
    return render(request, 'dashboard/embed_api.html')
    
def new_dateranges(request):
    return render(request, 'dashboard/name.html')

def get_name(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = NameForm(request.POST)
        dateForm = DateForm(request.POST)
        typeForm = TypeForm(request.POST)
        print ("HERE")
        # check whether it's valid:
        if dateForm.is_valid() and form.is_valid():# and typeForm.is_valid() and form.is_valid() :
            print ("HERE")
            select = form.cleaned_data['something']
            d_start = dateForm.cleaned_data['n_start']
            d_end = dateForm.cleaned_data['n_end']
            p_start = dateForm.cleaned_data['p_start']
            p_end = dateForm.cleaned_data['p_end']
            print ('select: ',select)
            #rep_type = typeForm.cleaned_data['rep_type']
            #print("SELECTED: ", select)
            print ('Start: ', str(d_start))
            print ('End: ', str(d_end))
            print ('Start: ', p_start)
            print ('End: ', p_end)
            #print ('Report By: ', rep_type)
            # process the data in form.cleaned_data as required
            # ...
            path = str(os.path.dirname(os.path.realpath('ga_nosampling_example_test1.py'))) + '\ga_nosampling_example_test1.py'
            #start(str(p_start), str(p_end), 2)
            # redirect to a new URL:
            ga_nosampling_example_test1.start(str(d_start), str(d_end), str(p_start), str(p_end), path, select)
            
            return render(request, 'dashboard/report.html', something(str(d_start), str(d_end), str(p_start), str(p_end), select))#{'current': current, 'previous': previous})#

    # if a GET (or any other method) we'll create a blank form
    else:
        form = NameForm()
        dateForm= DateForm()
        typeForm = TypeForm()

    return render(request, 'dashboard/name.html', {'form': form, 'date': dateForm, 'rep_type':typeForm})