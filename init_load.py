import psycopg2
import configparser
import requests
import json
import os
from datetime import datetime, timedelta
from datetime import date
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
    
    if mode == 'init':
        since_date_str = config.get('Payload', 'since')
        since_date = datetime.strptime(since_date_str, '%Y-%m-%d').date()
        until_date_str = config.get('Payload', 'until')
        until_date = datetime.strptime(until_date_str, '%Y-%m-%d').date()
        
        # Calculate the number of years to loop through
        num_years = until_date.year - since_date.year + 1

        all_data = []
        for i in range(num_years):
            start_year = since_date.year + i
            end_year = start_year + 1
            
            start_date = date(start_year, since_date.month, since_date.day)
            end_date = date(end_year, since_date.month, since_date.day) - timedelta(days=1)
            
            # Make sure we don't exceed the until_date
            if end_date > until_date:
                end_date = until_date
            
            start_date_str = start_date.strftime('%Y-%m-%d')
            end_date_str = end_date.strftime('%Y-%m-%d')
            
            workspaces = get_workspaces(api_token)
            data = []
            for workspace in workspaces:
                workspace_id = workspace['id']
                report_data = get_detailed_report(api_token, workspace_id, start_date_str, end_date_str)
                data.extend(report_data)
                print(f'Inserted data for workspace {workspace_id} from {since_date} to {since_date.year + 1}')
            
            all_data.extend(data)
        
        df = process_data(all_data)
        df.to_csv(f'toggl_data_init.csv', index=False)

    else:  # mode is 'recurring'
        days_back = config.getint('Download', 'recurring_days_back')
        until_date = datetime.today()
        since_date = (until_date - timedelta(days=days_back)).strftime('%Y-%m-%d')
        until_date = until_date.strftime('%Y-%m-%d')

if __name__ == "__main__":
    main()