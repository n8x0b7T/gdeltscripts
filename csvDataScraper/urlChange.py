from asyncore import file_dispatcher
import csv
import hashlib
import os
import re
import time
import urllib

from calendar import c
from urllib.parse import uses_fragment
from urllib.request import urlopen
from webbrowser import get
from xml.sax.saxutils import prepare_input_source
import requests
from io import BytesIO

from io import StringIO
from zipfile import ZipFile


# setting the URL the user wants to monitor...

req_headers = {'User-Agent': 'Mozilla/5.0'}


def extract_zip(input_zip):
    input_zip = ZipFile(input_zip)
    return {name: input_zip.read(name) for name in input_zip.namelist()}


def getCSV():
    last_update_url = 'http://data.gdeltproject.org/gdeltv2/lastupdate-translation.txt'
    r = requests.get(last_update_url,
                     headers=req_headers)

    zip_url = r.text.split("/n")[0].split(" ")[2].split("\n")[0]

    print(zip_url)


    request = requests.get(zip_url)
    file = ZipFile(BytesIO(request.content))

    print(file.read(file.filelist[0]))


getCSV()

exit()


# Performing a GET request and load the content
# of the website and store it in a variable
response = urlopen(url).read()

# Creating the initial hash...

current_hash = hashlib.sha224(response).hexdigest()
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
        # notify
        print("something changed")

        # again read the website
        response = urlopen(url).read()

        # create a hash
        currentHash = hashlib.sha224(response).hexdigest()

        # Wait for 30 seconds
        time.sleep(30)
        continue
