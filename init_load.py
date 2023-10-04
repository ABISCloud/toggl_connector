# Script to download data from Toggl and insert it into PostgreSQL
import psycopg2
import configparser
import requests
import json
import os
from datetime import datetime, timedelta
import pandas as pd

def get_workspaces(api_token):
    headers = {
        "Content-Type": "application/json",
    }
    response = requests.get(
        'https://api.track.toggl.com/api/v9/workspaces',
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
            "id" : item.get("id", ""),
            "user_name": item.get("user", ""),
            "Client": item.get("client", ""),
            "Project": item.get("project", ""),
            "Description": item.get("description", ""),
            "Billable": item.get("is_billable", ""),
            "Start_date": item["start"].split('T')[0] if "start" in item else "",
            "Start_time": item["start"].split('T')[1].split('+')[0] if "start" in item else "",
            "End_date": item["end"].split('T')[0] if "end" in item else "",
            "End_time": item["end"].split('T')[1].split('+')[0] if "end" in item else "",
            "Duration_ms": item.get("dur", ""),
            "Tags": item["tags"] if "tags" in item and item["tags"] else []
        }
        processed_data.append(processed_item)
    return pd.DataFrame(processed_data)

def main():
    config = configparser.ConfigParser()
    config.read('config.ini')
    api_token = config.get('Toggl', 'api_token')
    mode = config.get('Download', 'mode')
    year = config.get('Payload', 'since')[0:4]

    if mode == 'init':
        since_date = config.get('Payload', 'since')
        until_date = config.get('Payload', 'until')
    else:  # mode is 'recurring'
        days_back = config.getint('Download', 'recurring_days_back')
        until_date = datetime.today()
        since_date = (until_date - timedelta(days=days_back)).strftime('%Y-%m-%d')
        until_date = until_date.strftime('%Y-%m-%d')


    host = config.get('PostgreSQL', 'host')
    dbname = config.get('PostgreSQL', 'dbname')
    user = config.get('PostgreSQL', 'user')
    password = config.get('PostgreSQL', 'password')


    workspaces = get_workspaces(api_token)
    data = []
    for workspace in workspaces:
        workspace_id = workspace['id']
        report_data = get_detailed_report(api_token, workspace_id, since_date, until_date)
        data.extend(report_data)
        print(f'Inserted data for workspace {workspace_id} from {since_date} to {until_date}')

    df = process_data(data)
    df.to_csv(f'toggl_data_{year}.csv', index=False)
    print(df.head(100))

if __name__ == "__main__":
    main()
# save the data to a csv file


