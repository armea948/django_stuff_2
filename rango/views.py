from django.shortcuts import render
from django.http import HttpResponse
## from the ga_nosampling_example
from rango.models import GA_Data
import csv

def something():
    profile_ids = {'Bonia Indonesia':  '121438335'}
    ctr = 0
    for profile in sorted(profile_ids):
        path = 'bonia' #replace with path to your folder where csv file with data will be written
        filename = 'google_analytics_data_%s_1.csv'
    with open((path + filename %profile.lower()), "r", newline ='') as customersFile:
        reader = csv.reader(customersFile)   
        for row in reader:
            if ctr == 0:
                ctr = 1
            else:
                print("row: ", row)
                print("row[0]", row[0])
                addToModel = GA_Data(source = row[0], pageview = int(row[1]), bouncerate = float(row[2]), transactions = int(row[3]))
                try:
                    addToModel.save()
                except:
                    print("There's a problem with the line.")

            
def index(request):
  #context_dict = {'boldmessage': "I am bold font from the context"}
  #return render(request, 'rango/index.html', context_dict)
    #something()
    data = GA_Data.objects.all()
    if not data:
        something()
        print("EMPTY")
    
    return render(request, 'rango/data.html', {'data' :data})
  #return HttpResponse("Rango says hey there world!")
  
def about(request):
    return HttpResponse("Rango says here is the about page!")
# Create your views here.

   
