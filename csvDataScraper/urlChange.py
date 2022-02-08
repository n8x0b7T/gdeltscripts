import csv
import hashlib
import os
import re
import time
import urllib

from calendar import c
import requests
from io import BytesIO
from zipfile import ZipFile


# setting the URL the user wants to monitor...
r = requests.get('http://data.gdeltproject.org/gdeltv2/lastupdate-translation.txt',
headers={'User-Agent': 'Mozilla/5.0'})

print(r.text.split("/n")[0].split(" ")[2])


# Performing a GET request and load the content
# of the website and store it in a variable

response = urlopen(url).read()

# Creating the initial hash...

currentHash = hashlib.sha224(response).hexdigest()
print("running")
time.sleep(10)
while True:
    # Performing the get request and storing it in a variable
        response = urlopen(url).read()

        # Creating a hash...
        currentHash = hashlib.sha224(response).hexdigest()

        # Wait for 30 seconds...
        time.sleep(30)

        # Perform the get request...
        response = urlopen(url).read()

        # Creating a new hash...
        newHash = hashlib.sha224(response).hexdigest()

        # Checking to see if the new hash is the same
        # as the previous hash
        if newHash == currentHash:
            request = get('')


        # If something changed in the hashes
        else:
            #notify
            print("something changed")

            # again read the website
            response = urlopen(url).read()

            # create a hash
            currentHash = hashlib.sha224(response).hexdigest()

            # Wait for 30 seconds
            time.sleep(30)
            continue