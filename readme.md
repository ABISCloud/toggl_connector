
# Toggl Connector

This script is used to fetch and download reports from Toggl's Detailed Reports API, using a user-provided API token.

## Installation

1. Install Python: You can download the latest version of Python from [https://www.python.org/downloads/](https://www.python.org/downloads/). During the installation, make sure to check the box that adds Python to your `PATH`.

2. Install required Python modules: This script requires the `requests` and `configparser` Python modules. You can install these using pip, which is a package manager for Python. Open the command prompt on your server and run the following commands:

```cmd
pip install requests configparser
```

If you have both Python 2.x and Python 3.x versions on your server, and your script is written for Python 3.x, you might need to use `pip3` instead:

```cmd
pip3 install requests configparser
```

## Configuration

1. You need to create a `config.ini` file in the same directory as your Python script, with the following structure:

```ini
[Toggl]
api_token = your_api_token

[Payload]
since = yyyy-mm-dd
until = yyyy-mm-dd

[Download]
directory = path_to_save_csv_files
mode = init or recurring
recurring_days_back = number_of_days_back_for_recurring_mode
```

2. Replace `your_api_token` with your actual Toggl API token, which you can find in your Toggl Profile settings.

3. Replace `yyyy-mm-dd` in `since` and `until` with the actual dates for which you want to download the report. For `init` mode, this will be the entire timeframe you want to download, and for `recurring` mode, this will be the earliest timeframe you want the recurring downloads to start from.

4. Replace `path_to_save_csv_files` with the actual directory where you want the downloaded CSV files to be saved.

5. Set `mode` to either `init` for a one-time download of all data within the specified timeframe, or `recurring` for recurring downloads of the last few days of data.

6. Replace `number_of_days_back_for_recurring_mode` with the number of days in the past you want to fetch data for in `recurring` mode.

## Running the script

You can run the script using the following command in the command prompt:

```cmd
python get_reports.py
```

## Automating the script

If you want to run this script automatically at regular intervals, you can use the Task Scheduler on Windows or cron jobs on Unix-based systems. Alternatively, you could run the script in a cloud environment like an Azure function.
