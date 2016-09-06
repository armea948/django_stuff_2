"""Simple intro to using the Google Analytics API v3.
This application demonstrates how to use the python client library to access
Google Analytics data. The sample traverses the Management API to obtain the
authorized user's first profile ID. Then the sample uses this ID to
contstruct a Core Reporting API query to return the top 25 organic search
terms.
Before you begin, you must sigup for a new project in the Google APIs console:
https://code.google.com/apis/console
Then register the project to use OAuth2.0 for installed applications.
Finally you will need to add the client id, client secret, and redirect URL
into the client_secrets.json file that is in the same directory as this sample.
Sample Usage:
  $ python hello_analytics_api_v3.py
Also you can also get help on all the command-line flags the program
understands by running:
  $ python hello_analytics_api_v3.py --help
"""

__author__ = 'api.nickm@gmail.com (Nick Mihailovski)'


import argparse
import sys
import csv
import string

from apiclient.errors import HttpError
from apiclient import sample_tools
from oauth2client.client import AccessTokenRefreshError
from dashboard.models import GA_Data
from django.core.exceptions import ObjectDoesNotExist

profile_ids = {'Bonia Indonesia':  '121438335'}

class SampledDataError(Exception): pass


def main(argv, profile):
    ctr = 0
  # Authenticate and construct service.
    print('argv: ', argv)
    service, flags = sample_tools.init(argv, 'analytics', 'v3', __doc__, __file__, scope='https://www.googleapis.com/auth/analytics.readonly')
  # Try to make a request to the API. Print the results or handle errors.
    try:
        profile_id = profile_ids[profile]
        if not profile_id:
            print ('Could not find a valid profile for this user.')
        else:
            for start_date, end_date in date_ranges:
                limit = ga_query(service, profile_id, 0,
                                 start_date, end_date).get('totalResults')
                for pag_index in range(0, limit, 10000):
                    results = ga_query(service, profile_id, pag_index,
                                     start_date, end_date)
                    if results.get('containsSampledData'):
                        raise SampledDataError
                    print_results(results, pag_index, start_date, end_date, profile)
                    ctr = ctr + 1
        #print ("Total row: ", len(results))
    except TypeError as error:    
    # Handle errors in constructing a query.
        print ('There was an error in constructing your query : %s' % error)

    except HttpError as error:
    # Handle API errors.
        print ('Arg, there was an API error : %s : %s' %
           (error.resp.status, error._get_reason()))

    except AccessTokenRefreshError:
    # Handle Auth errors.
        print ('The credentials have been revoked or expired, please re-run '
           'the application to re-authorize')
  
    except SampledDataError:
    # force an error if ever a query returns data that is sampled!
        print ('Error: Query contains sampled data!')


def ga_query(service, profile_id, pag_index, start_date, end_date):
    return service.data().ga().get(
      ids='ga:' + profile_id,
      start_date=start_date,
      end_date=end_date,
      metrics='ga:pageviews, ga:bounceRate, ga:transactions, ga:sessions, ga:impressions',
      dimensions='ga:source',
      sort='-ga:pageviews',
      samplingLevel='HIGHER_PRECISION',
      start_index=str(pag_index+1),
      max_results=str(pag_index+10000)).execute()
      

def print_results(results, pag_index, start_date, end_date, profile):
    """Prints out the results.
    This prints out the profile name, the column headers, and all the rows of
    data.c
    Args:
        results: The response returned from the Core Reporting API.
    """
    total = [0.0, 0.0, 0.0, 0.0, 0.0]
    ctr = 0
    # New write header
    path = 'bonia' #replace with path to your folder where csv file with data will be written
    filename = 'google_analytics_data_%s_%d.csv' #replace with your filename. Note %s is a placeholder variable and the profile name you specified on row 162 will be written here
    with open(path + filename %(profile.lower(), 1), 'a') as f:
        writer = csv.writer(f, lineterminator='\n')
        if pag_index == 0:
            if (start_date, end_date) == date_ranges[0]:
                print ('Profile Name: %s' % results.get('profileInfo').get('profileName'))
                columnHeaders = results.get('columnHeaders')
                cleanHeaders = [str(h['name']) for h in columnHeaders]
                writer.writerow(cleanHeaders)
            print ('Now pulling data from %s to %s.' %(start_date, end_date))



  # Print data table.
        if results.get('rows', []):
            for row in results.get('rows'):
                for i in range(len(row)):
                    old, new = row[i], str()
                    for s in old:
                        new += s if s in string.printable else ''
                    row[i] = new
                    if i != 0:
                        total[i-1] = float(total[i-1]) + float(row[i])
                #writer.writerow(row)
                ctr = ctr + 1
                
            print ("row: ", row)
    
        else:
            print ('No Rows Found')
        writer.writerow(total)
        limit = results.get('totalResults')
        print (pag_index, 'of about', int(round(limit, -4)), 'rows.')
    print ("Total row: ", ctr)
    print("PROFILE: ", profile)
    try:
        GA_Data.objects.filter(date_start__exact=start_date).filter(date_end__exact=end_date).get()
        print("try-except")
    except ObjectDoesNotExist:
        addToModel = GA_Data(pageview = total[0], bouncerate = total[1], transactions = total[2], date_start= start_date, date_end=end_date)
        addToModel.save()
    print ("Hehe..")
    print (total)
    return None


##profile_ids = profile_ids = {'My Profile 1':  '1234567',
                             #'My Profile 2':  '1234568',
			     #'My Profile 3':  '1234569',
                             #'My Profile 4':  '1234561'}

# Uncomment this line & replace with 'profile name': 'id' to query a single profile
# Delete or comment out this line to loop over multiple profiles.
def start(s1, e1, s2, e2, path):
    global date_ranges
    date_ranges= [(s1,e1),(s2,e2)]
    print (date_ranges)
    for profile in sorted(profile_ids):
        print('enter main')
        #if __name__ == '__main__': 
        #main(sys.argv, profile, ctr)
        main([path], profile)
        print ('leave main')
        print ("Profile done. Next profile...")
        
    
    print ("All profiles done.")



#date_ranges = [('2016-06-01',
#               '2016-06-30')]#,
               # ('2015-10-01',
               # '2015-10-31'),
               # ('2015-11-01',
                # '2015-11-30',
               # ('2015-12-01',
               # '2015-12-31')]

#s = input("Date Started [yyyy-mm-dd]: ")
#e = input("Date Ended [yyyy-mm-dd]: ")
date_ranges = []
#start(s,e, 1)