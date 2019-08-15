import json
import requests
import argparse
from requests.auth import HTTPBasicAuth
import urllib3
urllib3.disable_warnings()

parser = argparse.ArgumentParser(description='Query the Ground Labs API to get details about a match. Outputs in CSV format.')
parser.add_argument('--username',nargs='?',required=True)
parser.add_argument('--password',nargs='?',required=True)
parser.add_argument('--api',nargs='?',required=True,help="The API endpoint...e.g. 'https://10.25.85.12:8339'")
args = parser.parse_args()

def subpath_generator(dict_var):
    if "subpaths" in dict_var:
        for path in dict_var["subpaths"]:
           for a in subpath_generator(path):
               yield a
    if "id" in dict_var:
        yield dict_var["id"]

print('Hostname,Group,Path,Data Type,Match,Prohibited,Creation Time,Modified Time,Owner,Location_Description,Target ID,Location ID,Object ID')

#Get group id
response = requests.get("{}/beta/groups".format(args.api,args),auth=HTTPBasicAuth(args.username,args.password),verify=False)
groups = json.loads(response.text)

for group in groups:
    gid = group["id"]
    gname = group["name"]

    #Get targets in group
    response = requests.get("{}/beta/groups/{}/targets?limit=100000".format(args.api,gid),auth=HTTPBasicAuth(args.username,args.password),verify=False)
    targets =  json.loads(response.text)

    for host in targets:
        if int(host["matches"]["match"]) > 0 or int(host["matches"]["prohibited"]) > 0:
            response = requests.get("{}/beta/targets/{}/locations".format(args.api,host["id"]),auth=HTTPBasicAuth(args.username,args.password),verify=False)
            locations =  json.loads(response.text)
            for location in locations:
                response = requests.get("{}/beta/targets/{}/matchobjects?details=true&location_id={}&limit=100000".format(args.api,host["id"],location["id"]),auth=HTTPBasicAuth(args.username,args.password),verify=False)
                matches = json.loads(response.text)
                for match in matches:
                    for _ in subpath_generator(match):
                        objectid = _
                        #Get details for each match id
                        response = requests.get("{}/beta/targets/{}/matchobjects/{}?details=true&limit=100000".format(args.api,host["id"],objectid),auth=HTTPBasicAuth(args.username,args.password),verify=False)
                        detail = json.loads(response.text)

                        created = "Unknown"
                        modified = "Unknown"
                        owner = "Unknown"
                        for label in detail["metas"]:
                            if label["label"] == "File Modified":
                                modified = label["value"]
                            if label["label"] == "File Created":
                                created = label["value"]
                            if label["label"] == "File Owner":
                                owner = label["value"]
                        for detailmatch in detail["matches"]:
                            try:
                                print('{name},{group},{path},{data_type},{content},{prohibited},"{created}","{modified}","{owner}","{location}",{targetid},{locationid},{objectid}'.format(name=host["name"],group=gname,path=match["path"],data_type=detailmatch["data_type"],content=detailmatch["content"],prohibited=detailmatch["severity"],created=created,modified=modified,owner=owner,location=location["description"],targetid=host["id"],locationid=location["id"],objectid=objectid))
                            except:
                                print("Error with host {}: {} {}".format(host["name"],match,detailmatch))
