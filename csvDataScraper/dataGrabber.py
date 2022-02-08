import csv
import hashlib
from multiprocessing.sharedctypes import Value
import os
import time
import urllib
from urllib import request
import requests

def dataGrab():
    # setting the URL the user wants to monitor...
    url = 'http://data.gdeltproject.org/gdeltv2/lastupdate-translation.txt'

    # Performing a GET request and load the content
    # of the website and store it in a variable
    r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, allow_redirects=True)

    csvMasterFile = open('csvMasterFile', 'w').write(r.content)

    # Prompting the user the data collection has begun
    print("Collection of GDELT CSV Translingual Data has begun...")
    print("To break the collection sequence, enter '0'...")
    value = "1"

    while (value != "0"):
        response = requests(r).read()

         # Creating the initial hash...
        currentHash = hashlib.sha224(response).hexdigest()
        print("running")
        time.sleep(10) 

        # Nested While-Loop used to test age of the webpage
        while True:
            # Performing the get request again and storing it in 'response'
            response = requests(r).read()

            #Creating a hash
            currentHash = hashlib.sha224(response).hexdigest()

            # Wait for the 15 minute update...
            time.sleep(900)

            # Perform the get request
            response = requests(r).read()

            # Creating a new hash...again
            newHash = hashlib.sha224(response).hexdigest()

            # Checking to see if the new hash is the same as the previous hash
            if newHash != currentHash:

                # Redefining the original URL, opening its contents,
                # and writing them to the master file

                csvurl = r.text.split("/n")[0].split(" ")[2]
                respone = request(csvurl).read()
                csvMasterFile.write(respone)
            
            # To test the URL change again
            else:
                print("Hashes remained the same...")
                continue

        value = input("Do you wish to continue running the GDELT 2.0 CSV Data Collector?" +
                    " Enter '1' for yes and '0' for no.")
    

             





