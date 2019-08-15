import json
import requests
import argparse
from requests.auth import HTTPBasicAuth
import urllib3
urllib3.disable_warnings()

parser = argparse.ArgumentParser(description='Get a list of all filters.')
parser.add_argument('--username',nargs='?',required=True)
parser.add_argument('--password',nargs='?',required=True)
parser.add_argument('--api',nargs='?',required=True,help="The API endpoint...e.g. 'https://10.25.85.12:8339'")
args = parser.parse_args()


response = requests.get("{}/beta/filters?limit=100000".format(args.api),auth=HTTPBasicAuth(args.username,args.password),verify=False)
agents = json.loads(response.text)

#['id', 'type', 'expression', 'apply_to'])
print("id,type,expression,apply_to")
for agent in agents:
    if "apply_to" not in agent:
        agent["apply_to"] = "Unknown"
    print("{},{},{},{}".format(agent["id"],agent["type"],agent["expression"],agent["apply_to"]))
