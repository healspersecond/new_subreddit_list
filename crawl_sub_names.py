import requests
import csv
import time
#import nltk
#from nltk.corpus import stopwords
import pandas as pd
#from bs4 import BeautifulSoup
import re
from pprint import pprint
from requests_toolbelt import user_agent
from requests import Session

# Prompts the user for User-Agent info to create custom header
user_agent_name = str(input("What is your User-Agent name?: "))
script_name = str(input("What is your script called?: "))
script_vers = str(input("What's the version number of this script (e.g, 0.0.1)?: "))
my_script = "{}/{}".format(script_name, script_vers)

s = Session()
s.headers = { 
    'User-Agent': user_agent(user_agent_name, my_script)
    }

# Define functions to parse json 
header = ['display_name']

def parse_response(User):
    pprint(display_name())
    return data

def display_name():
    result = data['data']['children'][n]['data']['display_name']
    return result

results = [] #Declared list
dict = {}   #Declared dictionary

# The URL to directly crawl the API---feel free to change it to your desired API endpoint
request_url = 'https://www.reddit.com/subreddits/new.json?limit=100'
r = requests.get(request_url, headers= s.headers)
data = r.json()
after_token = data['data']['after']

sub_number = len(data['data']['children'])
sub_num_seq = list(range(0,sub_number))

for item in header:
    for n in sub_num_seq :
        dict[item] = data['data']['children'][n]['data'][item]
        results.append(dict)#[item])

# Input command to determine how many pages of this specific API endpoint do you want to crawl
times_run =  int(input("How many pages do you want to crawl?: "))

with open('subreddit_list.tsv', 'w') as csvfile:
    fieldnames = results[0].keys()
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter='\t')
    writer.writeheader()


    i = 1
    while i <= times_run:
        if after_token == None:
            print("End of list at: ",i-1)
            break
        else:
            request_url = 'https://www.reddit.com/subreddits/new.json?limit=100&after='+after_token
            response = requests.get(request_url)
            if response.status_code != 200: #could also check == requests.codes.ok
                continue
            else:
                r = requests.get(request_url, headers= s.headers)
                data = r.json()
                sub_number = len(data['data']['children'])
                sub_num_seq = list(range(0,sub_number))
                after_token = data['data']['after']
                   
                for item in header:
                    for n in sub_num_seq:
                        dict[item] = data['data']['children'][n]['data'][item]
                        results.append(dict[item])
                        writer.writerow(dict)  #add to list
                print("Request ", i, " completed! after_token: ", after_token) # If the code breaks or server goes down, this last token can be used in the request_url to pick up where you left off
                i = i + 1
                time.sleep(.1)
        
    
## IMPORTANT NOTE ##

# If for some reason the server kicks us off or blocks calls, we will still know the last "after_token".
# This means that we can start the crawl again but from that last token, so we're not having to double over our previous calls.