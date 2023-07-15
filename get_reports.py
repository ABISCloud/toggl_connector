import configparser
import requests
import json
import csv
import os
from datetime import datetime, timedelta

def get_workspaces(api_token):
    headers = {
        "Content-Type": "application/json",
    }
    response = requests.get(
        'https://api.track.toggl.com/api/v8/workspaces',
        headers=headers,
        auth=(api_token, 'api_token')
    )
    response.raise_for_status()
    return response.json()

def get_detailed_report(api_token, workspace_id, since_date, until_date):
    report_data = []
    headers = {
        "Content-Type": "application/json",
    }
    page = 1
    while True:
        response = requests.get(
            f'https://api.track.toggl.com/reports/api/v2/details?workspace_id={workspace_id}&since={since_date}&until={until_date}&user_agent=api_test&page={page}',
            headers=headers,
            auth=(api_token, 'api_token')
        )
        response.raise_for_status()
        data = response.json()
        report_data.extend(data['data'])

        print(f'Successfully fetched page {page}')
        page += 1

        if not data['data']:
            break
    return report_data

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

def download_report(data, workspace_id, directory, mode, since_date, until_date):
    date_str = f'{since_date}_to_{until_date}'
    file_path = os.path.join(directory, f"toggl_report_{workspace_id}_{mode}_{date_str}.csv")
    with open(file_path, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)

def main():
    config = configparser.ConfigParser()
    config.read('config.ini')
    api_token = config.get('Toggl', 'api_token')
    mode = config.get('Download', 'mode')

    if mode == 'init':
        since_date = config.get('Payload', 'since')
        until_date = config.get('Payload', 'until')
    else:  # mode is 'recurring'
        days_back = config.getint('Download', 'recurring_days_back')
        until_date = datetime.today()
        since_date = (until_date - timedelta(days=days_back)).strftime('%Y-%m-%d')
        until_date = until_date.strftime('%Y-%m-%d')

    directory = config.get('Download', 'directory')

    workspaces = get_workspaces(api_token)
    for workspace in workspaces:
        workspace_id = workspace['id']
        report_data = get_detailed_report(api_token, workspace_id, since_date, until_date)
        processed_data = process_data(report_data)
        download_report(processed_data, workspace_id, directory, mode, since_date, until_date)
        print(f'Downloaded report for workspace {workspace_id} from {since_date} to {until_date}')

if __name__ == "__main__":
    main()
