## Purpose
The purpose of this code is to fetch detailed time entries from Toggl API and store them in a PostgreSQL database.

## Dependencies
This code requires the following dependencies:
- psycopg2
- configparser
- requests
- json
- os
- datetime

## Functions
This code contains the following functions:

### get_workspaces(api_token)
This function takes an API token as input and returns a list of workspaces associated with the Toggl account.

### get_detailed_report(api_token, workspace_id, start_date, end_date)
This function takes an API token, workspace ID, start date, and end date as input and returns a list of detailed time entries for the specified workspace and time period.

### process_data(data, conn)
This function takes a list of time entries and a PostgreSQL connection object as input and inserts the time entries into the PostgreSQL database.

### main()
This function is the main function that executes the code. It reads the configuration file, fetches the workspaces, fetches the detailed time entries for each workspace, and inserts the time entries into the PostgreSQL database.

## Configuration
This code requires a configuration file named `config.ini` in the same directory as the code. The configuration file should contain the following sections and options:

### Toggl
- api_token: The API token for the Toggl account.

### Download
- mode: The mode for downloading time entries. Currently, only "detailed" mode is supported.

### Payload
- start_date: The start date for downloading time entries in the format "YYYY-MM-DD".
- end_date: The end date for downloading time entries in the format "YYYY-MM-DD".

### PostgreSQL
- host: The hostname for the PostgreSQL database.
- dbname: The name of the PostgreSQL database.
- user: The username for the PostgreSQL database.
- password: The password for the PostgreSQL database.

## Execution
To execute the code, simply run the `main()` function. The code will fetch the detailed time entries for each workspace associated with the Toggl account and insert them into the PostgreSQL database.