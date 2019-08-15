import json
import requests
import argparse
from requests.auth import HTTPBasicAuth
import urllib3
urllib3.disable_warnings()
import csv

parser = argparse.ArgumentParser(description='Remediate files.')
parser.add_argument('--username',nargs='?',required=True)
parser.add_argument('--password',nargs='?',required=True)
parser.add_argument('--api',nargs='?',required=True,help="The API endpoint...e.g. 'https://10.25.85.12:8339'")
parser.add_argument('--file',nargs='?',required=True,help="The csv file containing remediation instructions")
args = parser.parse_args()

print("target_id,path,status,response")
with open(args.file, newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        json={"path":row["path"],"sign_off":row["sign_off"],"object_ids":row["object_ids"].split(),"reason":row["reason"],"password":row["password"]}
        print("{},{}".format(row["target_id"],row["path"]),end='')
        response = requests.post("{api}/beta/targets/{target_id}/locations/{location_id}/remediation/{action}".format(api=args.api,target_id=row["target_id"],location_id=row["location_id"],action=row["action"]),json=json,auth=HTTPBasicAuth(args.username,args.password),verify=False)
        print(',{},"{}"'.format(response.status_code,response.text.replace('"','\\"')))

