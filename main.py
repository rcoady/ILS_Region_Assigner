import csv
import json
import urllib2
from secret import api


North = ["Boone County", "Ogle County", "Winnebago County"]
West_Central = ["Bureau County", "Fulton County", "Henry County", "Knox County", "Lasalle County", "Lee County",
                "Macoupin County", "Madison County", "McDonough County", "Montgomery County", "Morgan County",
                "Peoria County", "Putnam County", "Rock Island County", "Scott County", "St Clair County",
                "Tazewell County", "Warren County"]
Northwest = ["Carroll County", "Jo Daviess County", "Stephenson County", "Whiteside County"]
South = ["Champaign County","Edgar County", "Ford County", "Iroquois County", "Jackson County", "Kankakee County", "Logan County",
         "Macon County", "Mclean County", "Piatt County", "Sangamon County", "Shelby County", "Vermillion County"]
South_Central = ["Dekalb County", "Grundy County", "Kane County", "Kendall County"]
Central = ["Dupage County", "Will County"]
Northeast = ["Lake County", "McHenry County"]




filename = raw_input("Enter a file name: ")

if filename == '':
    filename = 'Alumni.csv'

f = open(filename, 'rU')
data = csv.reader(f)

word = 'County'

c = csv.writer(open("Address.csv", "wb"))

for row in data:

    if filename == 'Alumni.csv':
        primary_street = row[11]
        primary_city = row[12]
        primary_state = row[13]
    elif filename == 'Leaders2016.csv':
        primary_street = row[6]
        primary_city = row[7]
        primary_state = row[8]

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

    if primary_state == "Illinois" or primary_state == "IL":
        if county in North:
            region = "North"
        elif county in West_Central:
            region = "West Central"
        elif county in Northwest:
            region = "Northwest"
        elif county in South:
            region = "South"
        elif county in South_Central:
            region = "South Central"
        elif county in Central:
            region = "Central"
        elif county in Northeast:
            region = "Northeast"
        elif county == "Cook County":
            region = "Cook"
        else:
            region = "This county needs to be added"

    print region
    c.writerow([row[1], row[2], full_address, county, region])
print "The information has been saved to Address.csv"
