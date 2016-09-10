import csv
import json
import urllib2
from secret import api

filename = raw_input("Enter a file name:")

if filename == '':
    filename = 'Alumni.csv'

f = open(filename, 'rU')
data = csv.reader(f)

word = 'County'

c = csv.writer(open("Address.csv", "wb"))

for row in data:
    primary_street = row[11]
    primary_city = row[12]
    primary_state = row[13]

    primary_address = [primary_street, primary_city, primary_state]

    full_address = ", ".join(primary_address)

    geo_address = full_address.replace(" ", "+")

    url = "https://maps.googleapis.com/maps/api/geocode/json?address=%s&key=%s" % (geo_address, api)

    response = urllib2.urlopen(url)

    jsongeocode = json.loads(response.read())

    json_response = jsongeocode["results"][0]["address_components"]

    length = len(json_response)
    print full_address
    county = json_response[length - 5]["short_name"]

    if word not in county:
        county = json_response[length - 4]["short_name"]

    print county
    c.writerow([row[1], row[2], full_address, county])


