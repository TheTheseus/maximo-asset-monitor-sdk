#  | * IBM Confidential
#  | * OCO Source Materials
#  | * 5737-M66
#  | * © Copyright IBM Corp. 2020
#  | * The source code for this program is not published or otherwise divested of its
#  | * trade secrets, irrespective of what has been deposited with the U.S.
#  | * Copyright Office.

# python libraries
import json
import re
import importlib
import logging
from string import punctuation, whitespace
from sqlalchemy import Integer, String, Float, DateTime, Boolean, SmallInteger
from datetime import datetime

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

delimiter_pattern = "|".join([re.escape(delimiter) for delimiter in punctuation + whitespace + "t" + "T"])
compiled_delimiter_pattern = re.compile(delimiter_pattern)


def validateJSON(json_payload):
    """validate that the input parameter is a valid json file"""
    try:
        payload = json.loads(json_payload)
    except ValueError as err:
        return False
    return payload


def convert_to_datetime(timestamp_string):
    """convert string input to datetime.datetime type"""
    if timestamp_string is None:
        return None

    split_timestamp_string = compiled_delimiter_pattern.split(timestamp_string)

    timestamp_values = [int(value) for value in split_timestamp_string]
    return datetime(*timestamp_values)


def validate_and_normalize_timestamp(timestamp_string):
    """convert string input to datetime.datetime type"""
    if timestamp_string is None:
        return None

    datetime_timestamp = convert_to_datetime(timestamp_string)
    return datetime_timestamp.isoformat(sep=" ")


# converting user input 'type' to sqlalchemy type
_type_sql_dict = {
    'int': Integer,
    'integer': Integer,
    'string': String,
    'str': String,
    'float': Float,
    'number': Float,
    'datetime': DateTime,
    'bool': Boolean,
    'boolean': Boolean
}


def sqlalchemy_type(type):
    """Return the closest sql type for a given string"""
    if type in _type_sql_dict:
        return _type_sql_dict[type.lower()]
    else:
        raise NotImplementedError(
            "You may add custom `sqltype` to `" + str(type) + "` assignment in `_type_sql_dict`.")


# converting user input 'type' to python built-in type
_type_python_dict = {
    'int': int,
    'integer': int,
    'string': str,
    'str': str,
    'number': float,
    'float': float,
    'datetime': datetime,
    'bool': bool,
    'boolean': bool
}


def python_type(type):
    """Return the closest python type for a given string"""
    if type in _type_python_dict:
        return _type_python_dict[type.lower()]
    else:
        raise NotImplementedError(
            "You may add custom `datatype` to `" + str(type) + "` assignment in `_type_python_dict`.")


def generate_api_environment(credentials):
    """
    make desired environment from credentials
    sample environment:
    {
      "tenant_id": "AnalyticsServiceDev",
      "_comment_tenant_id": "REQUIRED. same as the one credentials.json",

      "base_url": "https://api-dev.connectedproducts.internetofthings.ibmcloud.com",
      "_comment_base_url": "REQUIRED",

      "version": "v1",
      "_comment_version": "OPTIONAL. default value is v1",

      "isBasicAuth": false,
      "_comment_isBasicAuth_1/3": "REQUIRED. default value is false. ",
      "_comment_isBasicAuth_2/3": "when true requires: API_USERNAME and API_PASSWORD when True. ",
      "_comment_isBasicAuth_3/3": "when false requires: authentication_header={'x-api-key', 'x-api-token'}",

      "authentication_header": {
        "X-api-key": "valid-api-key-goes-here",
        "X-api-token": "valid-api-token-goes-here"
      },
      "_comment_authentication_header": "REQUIRED",

      "disableCertificateVerification": true,
      "_comment_disableCertificateVerification_1/1": "OPTIONAL. default value is true"
    }
    '''
    :param credentials:
    :return: environment
    """

    if credentials is None:
        raise Exception("No credentials provided")

    environment = {'authentication_header': {}}

    if credentials['tenantId'] is None:
        raise RuntimeError(('No tenant id supplied in credentials'
                            ' Please supply a valid tenant id.'))
    else:
        environment['tenant_id'] = credentials['tenantId']

    if credentials['iotp'] is None:
        raise RuntimeError(('No iotp information supplied in credentials'
                            ' Please supply valid authentication/url information in `iotp` key'))
    else:
        if credentials['iotp']['apiKey'] is None:
            raise RuntimeError(('No api-key supplied in credentials'
                                ' Please supply valid api-key'))
        else:
            environment['authentication_header']['X-api-key'] = credentials['iotp']['apiKey']

        if credentials['iotp']['apiToken'] is None:
            raise RuntimeError(('No api-token supplied in credentials'
                                ' Please supply valid api-token'))
        else:
            environment['authentication_header']['X-api-token'] = credentials['iotp']['apiToken']

        if credentials['iotp']['asHost'] is None:
            raise RuntimeError(('No host url supplied in credentials'
                                ' Please supply valid host url'))
        else:
            environment['base_url'] = credentials['iotp']['asHost']

    return environment


# converting user input 'type' to python built-in type
_type_user_to_api_dict = {
    'int': 'NUMBER',
    'integer': 'NUMBER',
    'string': 'LITERAL',
    'str': 'LITERAL',
    'number': 'NUMBER',
    'float': 'NUMBER',
    'datetime': 'TIMESTAMP',
    'bool': 'BOOLEAN',
    'boolean': 'BOOLEAN'
}


def api_type(type):
    """Return the closest python type for a given string"""
    if type in _type_user_to_api_dict:
        return _type_user_to_api_dict[type.lower()]
    else:
        raise NotImplementedError(
            "You may add custom `datatype` to `" + str(type) + "` assignment in `_type_user_to_api_dict`.")
