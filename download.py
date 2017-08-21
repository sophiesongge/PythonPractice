#############################
#ProActive Catalog Migration#
#############################

import os
import sys
import json
import getopt
import shutil
import zipfile
import urllib.request as ur

def downloadWFs(bucket):
    bucketURL = bucket + "/workflows/"
    meta = json.load(ur.urlopen(bucket))
    name = meta.get("name")
    mypath = "./"+name
    if not os.path.isdir(mypath):
        os.makedirs(mypath)
    metaWorkflow = json.load(ur.urlopen(bucketURL))
    workflowList = metaWorkflow.get("_embedded").get("workflowMetadataList")
    print("Begin Downloading Bucket: " +name+" ...")
    for w in workflowList:
        wf = bucketURL + str(w.get("id"))
        wfmeta = json.load(ur.urlopen(wf))
        wfURL = wfmeta.get("_links").get("content").get("href")
        file_name = wfmeta.get("name")+".xml"
        fullfilename = os.path.join(mypath, file_name)
        u = ur.urlopen(wfURL)
        f = open(fullfilename, 'wb')
        f.write(u.read())
        f.close()
    print("Finish Downloading Bucket: "+name+".")

def zipBucket(bucket):
    bucketURL = bucket + "/workflows/"
    meta = json.load(ur.urlopen(bucket))
    name = meta.get("name")
    mypath = "./"+name
    myname = mypath + ".zip"
    zipf = zipfile.ZipFile(myname, 'w', zipfile.ZIP_DEFLATED)
    print("Begin Zipping Bucket: " +name+" ...")
    for root, dirs, files in os.walk(mypath):
        for file in files:
            zipf.write(os.path.join(root, file))
    print("Finish Zipping Bucket: "+name+".")
    
    if os.path.exists(mypath):
        shutil.rmtree(mypath)
    
    return os.path.abspath(myname)

def migration(catalogURL, path):
    if path == "./":
        path = os.path.abspath(os.curdir) + "/CatalogWorkflows"
    else:
        path = path + "/CatalogWorkflows"
    if not os.path.isdir(path):
        os.makedirs(path)    
    bucketsURL = catalogURL+"/buckets"
    metaBucket = json.load(ur.urlopen(bucketsURL))
    bucketList = metaBucket.get("_embedded").get("bucketMetadataList")
    for l in bucketList:
        bucket = bucketsURL+"/"+str(l.get("id"))
        downloadWFs(bucket)
        name = zipBucket(bucket)
        shutil.move(name, path+"/"+name.split('/')[-1])
    print("Migration Finished ...")
    
if __name__ == "__main__":    
    #catalogURL = "http://try.activeeon.com:8080/workflow-catalog"
    #path = "./catalog"
    catalogURL = ""
    path = ""
    opts, args = getopt.getopt(sys.argv[1:], "o:p:")
    for op, value in opts:
        if op == "-o":
            catalogURL = value 
        if op == "-p":
            path = value
    migration(catalogURL, path)
