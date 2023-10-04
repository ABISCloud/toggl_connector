## get users from a workspace
import requests
from base64 import b64encode
import configparser

# Read the config file
config = configparser.ConfigParser()
config.read('config.ini')

# Get the Toggl API credentials from the config file
email = config.get("Toggl", "email")
password = config.get("Toggl", "password")
workspace_id = config.get("Toggl", "workspace_id")
organization_id = config.get("Toggl", "organization_id")

# Get the workspace users
data = requests.get(f'https://api.track.toggl.com/api/v9/organizations/{organization_id}/workspaces/{workspace_id}/workspace_users', headers={'content-type': 'application/json', 'Authorization' : 'Basic %s' %  b64encode(f"{email}:{password}".encode("ascii")).decode("ascii")})
print(data.json())

# # display as a dataframe
# import pandas as pd
# df = pd.DataFrame(data.json())
# print(df.head(10))

# save as a csv
import csv

with open('toggl_workspace_users.csv', 'w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=data.json()[0].keys())
    writer.writeheader()
    writer.writerows(data.json())
