from mam.sdk import (entitytype,
                     constants,
                     kpifunction)
import json

#DEFINE PATH TO REQUIRED FILES
#relative to where you run script from
credentials_path = './dev_resources/credentials.json'
entitytype_data_path = './scripts/sample_usage_data.json'
constants_data_path = './scripts/sample_constant_data.json'
function_data_path = './scripts/sample_function_data.json'

#LOADING DATABASE CREDENTIALS
'''
# Getting and saving Db credentials
# Explore > Usage > Watson IOT Platform Analytics > Copy to clipboard
# Paste contents in credentials.json file
# Save file in maximo-asset-monitor-sdk/dev_resources folder (one example)
'''
print('Reading Analytics Credentials')
with open(credentials_path, 'r') as F:
    credentials = json.load(F)

"""-------------------------------ENTITY TYPE DEMO------------------------
Usage:
1. (X) Create Entity Type - using a json payload
------------------------------------------------------------------------"""
tests_completed = {'create_entity': False}
# 1. Sample Usage Module: Create Entity Type
with open(entitytype_data_path, 'r') as f:
    try:
        rc_create = entitytype.create_custom_entitytype(f.read(), credentials=credentials)
        print(f'rc is {rc_create}. \nCreate Entity Type test completed successfully')
        tests_completed['create_entity'] = True
    except Exception as msg:
        print(f'FAILED STEP: {msg}\nFailed create entity type test')


"""-------------------------------ADD FUNCTION TO ENTITY TYPE DEMO------------------------
Usage:
1. (X) Add Function - using a json payload
------------------------------------------------------------------------------------------"""
tests_completed ['add_functions'] = False
# 1. Sample Usage Module: Create Entity Type
with open(function_data_path, 'r') as f:
    try:
        rc_create = kpifunction.add_functions(f.read(), credentials=credentials)
        print(f'rc is {rc_create}. \nAdd KPI Functions test completed successfully')
        tests_completed['add_functions'] = True
    except Exception as msg:
        print(f'FAILED STEP: {msg}\nFailed add functions test')


"""-------------------------------CONSTANTS DEMO------------------------
Usage:
1. (X) Create Constants - using a json payload
----------------------------------------------------------------------"""
tests_completed['create_constants'] = False
# 1. Sample Usage Module: Create Constants
with open(constants_data_path, 'r') as f:
    try:
        rc_create = constants.create_constants(f.read(), credentials=credentials)
        print(f'rc is {rc_create}. \nCreate Constants test completed successfully')
        tests_completed['create_constants'] = True
    except Exception as msg:
        print(f'FAILED STEP: {msg}\nFailed create constants test')


"""-------------------------------SUMMARY OF CREATION TESTS------------------------
1. entitytype_tests_completed
2. functions_tests_completed
3. constants_tests_completed
---------------------------------------------------------------------------------"""
print('Summary of all tests run')
for name, status in tests_completed.items():
    print(f'Test {name} status {status}')