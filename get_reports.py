import configparser
import requests
from requests.auth import HTTPBasicAuth
import json
import csv
import os
from datetime import datetime

def get_workspaces(api_token):
    response = requests.get(
        'https://api.track.toggl.com/api/v9/workspaces',
        auth=HTTPBasicAuth(api_token, 'api_token')
    )
    response.raise_for_status()
    return response.json()

def get_detailed_report(api_token, workspace_id, payload):
    response = requests.get(
        f'https://api.track.toggl.com/reports/api/v2/details?user_agent=api_test&workspace_id={workspace_id}&since={payload["since"]}&until={payload["until"]}',
        auth=HTTPBasicAuth(api_token, 'api_token')
    )
    response.raise_for_status()
    return response.json()

def process_data(data):
    processed_data = []
    for item in data:
        processed_item = {
            "User": item.get("user", ""),
            "Email": "",  # Toggl Detailed Reports API does not return email
            "Client": item.get("client", ""),
            "Project": item.get("project", ""),
            "Description": item.get("description", ""),
            "Billable": item.get("is_billable", ""),
            "Start date": item["start"].split('T')[0] if "start" in item else "",
            "Start time": item["start"].split('T')[1].split('+')[0] if "start" in item else "",
            "End date": item["end"].split('T')[0] if "end" in item else "",
            "End time": item["end"].split('T')[1].split('+')[0] if "end" in item else "",
            "Duration": item.get("dur", ""),
            "Tags": ", ".join(item["tags"]) if "tags" in item else ""
        }
        processed_data.append(processed_item)
    return processed_data


def download_report(data, workspace_id, directory):
    file_path = os.path.join(directory, f"toggl_report_{workspace_id}.csv")
    with open(file_path, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)

def main():
    config = configparser.ConfigParser()
    config.read('config.ini')
    api_token = config.get('Toggl', 'api_token')

    payload = {
        "since": config.get('Payload', 'since'),
        "until": config.get('Payload', 'until')
    }

    directory = config.get('Download', 'directory')

    workspaces = get_workspaces(api_token)
    for workspace in workspaces:
        workspace_id = workspace['id']
        report_data = get_detailed_report(api_token, workspace_id, payload)
        processed_data = process_data(report_data['data'])
        download_report(processed_data, workspace_id, directory)
        print(f'Downloaded report for workspace {workspace_id}')

if __name__ == "__main__":
    main()
