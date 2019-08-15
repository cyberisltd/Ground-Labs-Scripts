import json
import requests
import argparse
from requests.auth import HTTPBasicAuth
import urllib3
urllib3.disable_warnings()

parser = argparse.ArgumentParser(description='Get a list of all targets.')
parser.add_argument('--username',nargs='?',required=True)
parser.add_argument('--password',nargs='?',required=True)
parser.add_argument('--api',nargs='?',required=True,help="The API endpoint...e.g. 'https://10.25.81.12:8339'")
args = parser.parse_args()

print('target_id,hostname,group,search_status,search_time,comments,matches,prohibited')

response = requests.get("{}/beta/groups".format(args.api),auth=HTTPBasicAuth(args.username,args.password),verify=False)
groups = json.loads(response.text)

for group in groups:
    response = requests.get("{}/beta/groups/{}/targets?limit=10000".format(args.api,group["id"]),auth=HTTPBasicAuth(args.username,args.password),verify=False)
    targets =  json.loads(response.text)
    for target in targets:
        response = requests.get("{}/beta/targets/{}".format(args.api,target["id"]),auth=HTTPBasicAuth(args.username,args.password),verify=False)
        detail =  json.loads(response.text)
        print("{},{},{},{},{},{},{},{}".format(target["id"],detail["name"],group["name"],detail["search_status"],detail["search_time"],detail["comments"],detail["matches"]["match"],detail["matches"]["prohibited"]))
