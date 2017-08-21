####################################
#ProActive Catalog Migration Upload#
####################################

import os
import sys
import json
import getopt
import requests
import urllib.request as ur

#####Walk through a directory and Create a bucket for each zip file, then upload this zip to the new created bucket######

def upload(rootDir, newCatalog):    
    buckets = newCatalog + 'buckets/'
    bucketURL = buckets+'?name='
    list_dirs = os.walk(rootDir)
    for root, dirs, files in list_dirs:
        for f in files:
            zipName = os.path.join(root, f).split('/')[-1]
            if(zipName.split('.')[-1] == 'zip'):
                bucketName =  zipName.split('.')[0]
                print("Begin uploading Bucket: "+bucketName)
                response = requests.post(bucketURL+bucketName)
                meta = json.load(ur.urlopen(buckets))
                bucketID = meta[-1].get('id')
                #print(meta[-1].get('id'))
                url = buckets+str(bucketID)+'/resources?kind=workflow&commitMessage=migration&contentType=zip'
                files = {'file': open(rootDir + zipName, 'rb')}
                r = requests.post(url, files=files)
        

if __name__ == "__main__":    
    #rootDir = '/Users/sophiesong/Desktop/CatalogWorkflows/'
    #newCatalog = 'https://tryqa.activeeon.com/catalog/'
    rootDir = ""
    newCatalog = ""
    opts, args = getopt.getopt(sys.argv[1:], "n:p:")
    for op, value in opts:
        if op == "-n":
            newCatalog = value 
        if op == "-p":
            rootDir = value
    upload(rootDir, newCatalog)