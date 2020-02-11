import json
import requests
import argparse
from requests.auth import HTTPBasicAuth
import urllib3
urllib3.disable_warnings()
import csv

parser = argparse.ArgumentParser(description='Schedule a scan.')
parser.add_argument('--username',nargs='?',required=True)
parser.add_argument('--password',nargs='?',required=True)
parser.add_argument('--api',nargs='?',required=True,help="The API endpoint...e.g. 'https://10.25.85.12:8339'")
parser.add_argument('--profile',nargs='?',default="8078594885656796410",help="The profile to use")
parser.add_argument('--file',nargs='?',required=True,help="The csv file containing scan instructions")
parser.add_argument('--start',nargs='?',required=True,help="YYYY-MM-DD hh:mm")
parser.add_argument('--label',nargs='?',required=True,help="Label for the scan")
args = parser.parse_args()

targets = {}
targetlist = []
with open(args.file, newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        if row["target_id"] not in targets:
            targets[row["target_id"]] = []
        targets[row["target_id"]].append({"id":row["location_id"],"subpath":row["subpath"]})
        if row["location_id2"]:
            targets[row["target_id"]].append({"id":row["location_id2"],"subpath":row["subpath2"]})
        
for target in targets:
    for location in targets[target]:
        targetlist.append({"id": target,"locations":targets[target]})

json={"label":args.label,"targets":targetlist,"profiles":[args.profile],"start":args.start}

response = requests.post("{api}/beta/schedules".format(api=args.api),json=json,auth=HTTPBasicAuth(args.username,args.password),verify=False)
print('{},{}'.format(response.status_code,response.text))

