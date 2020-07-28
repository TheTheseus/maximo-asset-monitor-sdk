#  | * IBM Confidential
#  | * OCO Source Materials
#  | * 5737-M66
#  | * © Copyright IBM Corp. 2020
#  | * The source code for this program is not published or otherwise divested of its
#  | * trade secrets, irrespective of what has been deposited with the U.S.
#  | * Copyright Office.

from mam.sdk import (alerts)
import json

# DEFINE PATH TO REQUIRED FILES
# relative to where you run script from
credentials_path = './dev_resources/credentials.json'
get_alerts_payload = './data/sample_alerts_data.json'

# LOADING DATABASE CREDENTIALS
'''
# Getting and saving Db credentials
# Explore > Usage > Watson IOT Platform Analytics > Copy to clipboard
# Paste contents in credentials.json file
# Save file in maximo-asset-monitor-sdk/dev_resources folder (one example)
'''
print('Reading Analytics Credentials')
with open(credentials_path, 'r') as F:
    credentials = json.load(F)

with open(get_alerts_payload, 'r') as payload:
    get_response = alerts.get_alerts(payload.read(), credentials)
    print(get_response)
