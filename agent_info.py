import json
import requests
import argparse
from requests.auth import HTTPBasicAuth
import urllib3
urllib3.disable_warnings()

parser = argparse.ArgumentParser(description='Get a list of all targets.')
parser.add_argument('--username',nargs='?',required=True)
parser.add_argument('--password',nargs='?',required=True)
parser.add_argument('--api',nargs='?',required=True,help="The API endpoint...e.g. 'https://10.25.85.12:8339'")
args = parser.parse_args()


response = requests.get("{}/beta/agents?limit=100000".format(args.api),auth=HTTPBasicAuth(args.username,args.password),verify=False)
agents = json.loads(response.text)

print("name,version,platform,proxy,connectedip,connected,boot,started,dev0ip,dev0mac")

for agent in agents:
    if "platform" not in agent:
        agent["platform"] = "Unknown"
    if "boot" not in agent:
        agent["boot"] = "Unknown"
    if "started" not in agent:
        agent["started"] = "Unknown"
    if "networks" not in agent:
        agent["networks"] = [] 
        agent["networks"].append({'ip':'Unknown','mac':'Unknown'})
    if "connected_ip" not in agent:
        agent["connected_ip"] = "Unknown"
    print('{},{},"{}",{},{},{},{},{},{},{}'.format(agent["name"],agent["version"],agent["platform"],agent["proxy"],agent["connected_ip"],agent["connected"],agent["boot"],agent["started"],agent["networks"][0]["ip"],agent["networks"][0]["mac"]))
