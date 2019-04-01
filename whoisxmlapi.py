'''
whoisxmlapi interface
@author: Erik Borra
@email: borra@uva.nl
'''

csv_file = ''  # one domain per line
cache_dir = '' # where to store json files
api_key = ''   # api key, get yours at https://user.whoisxmlapi.com/products

api_endpoint = "https://www.whoisxmlapi.com/whoisserver/WhoisService"
api_balance = "https://www.whoisxmlapi.com/accountServices.php?servicetype=accountbalance"

import pandas
import requests
import json
import os

# read csv file and clean domains
df = pandas.read_csv(csv_file)
df['domain'] = df['domain'].replace(r'https?://w?w?w?\.?', '', regex=True) # remove everything before the domain
df['domain'] = df['domain'].replace(r'\/.*', '', regex=True) # remove everything after the domain

# loop over domains and get whois data
for domain in df['domain']:
    # check if file is already cached
    filename = cache_dir + '/' + domain + '.json'
    exists = os.path.isfile(filename)
    if exists:
        print("already cached\t%s"%(domain))
        with open(filename, 'r') as myfile:
            data=myfile.read()
    # if not cached
    else:
        # check account balance
        params = {'apiKey':api_key,'output_format':'JSON'}
        r = requests.get(url = api_balance, params = params)
        json_balance = json.loads(r.text)
        # if enough on balance
        if json_balance['balance'] > 0:        
            # get whois
            print("balance %s\tretrieving %s"%(json_balance['balance'],domain))
            params = {'apiKey':api_key,"domainName":domain,"outputFormat":"JSON","preferFresh":"1","ip":"1","ipWhois":"1"} 
            r = requests.get(url = api_endpoint, params = params)
            # save whois as cache file
            with open(filename, 'w') as json_file:
                json.dump(json.loads(r.text), json_file)
        else:
            print("Balance = 0, top up your balance")
            break
print("done")
