#!/usr/bin/python3

import requests
import json
import re
from requests.models import HTTPError

url = "https://api.octopus.energy/v1/graphql/"
APIKeyPattern = re.compile('sk_live_[A-Za-z0-9]{24}?$')
accountNumberPattern = re.compile('A-[0-9A-F]{8}?$')

def validate_input(prompt, pattern):
    while True:
        user_input = input(prompt)
        if pattern.match(user_input):
            return user_input
        else:
            print("Invalid input. Please try again.")

accountNumber = validate_input("Enter account number: ", accountNumberPattern)
apikey = validate_input("Enter API key: ", APIKeyPattern)

def refreshToken(apiKey, accountNumber):
    try:
        query = """
        mutation krakenTokenAuthentication($api: String!) {
            obtainKrakenToken(input: {APIKey: $api}) {
                token
            }
        }
        """
        variables = {'api': apiKey}
        r = requests.post(url, json={'query': query, 'variables': variables})
    except HTTPError as http_err:
        print(f'HTTP Error {http_err}')
    except Exception as err:
        print(f'Another error occurred: {err}')

    jsonResponse = json.loads(r.text)

    if r.text.find("Authentication failed.") > -1:
        raise SystemExit("Authentication failed - check API key")
    else:
        return jsonResponse['data']['obtainKrakenToken']['token']

def print_json(json_data):
    for key, value in json_data.items():
        print(f"{key}:")
        if isinstance(value, list):
            for item in value:
                print("    -")
                for sub_key, sub_value in item.items():
                    print(f"        {sub_key}: {sub_value}")
        else:
            for sub_key, sub_value in value.items():
                print(f"    {sub_key}: {sub_value}")
        print()

def getObject():
    global authToken
    try:
        query = """
        query getData($input: String!) {
            plannedDispatches(accountNumber: $input) {
                startDt
                endDt
                delta
            }
        }
        """
        variables = {'input': accountNumber}
        headers = {"Authorization": authToken}
        r = requests.post(url, json={'query': query, 'variables': variables, 'operationName': 'getData'}, headers=headers)
        formatted_json = json.loads(r.text)['data']
        print_json(formatted_json)
        return formatted_json
    except HTTPError as http_err:
        print(f'HTTP Error {http_err}')
    except Exception as err:
        print(f'Another error occurred: {err}')
        pass

def getObjectCompleted():
    global authToken
    try:
        query = """
        query getData($input: String!) {
            completedDispatches(accountNumber: $input) {
                startDt
                endDt
                delta
            }
        }
        """
        variables = {'input': accountNumber}
        headers = {"Authorization": authToken}
        r = requests.post(url, json={'query': query, 'variables': variables, 'operationName': 'getData'}, headers=headers)
        formatted_json = json.loads(r.text)['data']
        print_json(formatted_json)
        return formatted_json
    except HTTPError as http_err:
        print(f'HTTP Error {http_err}')
    except Exception as err:
        print(f'Another error occurred: {err}')
        pass

def getObjectAccount():
    global authToken
    try:
        query = """
        query getData($input: String!) {
            registeredKrakenflexDevice(accountNumber: $input) {
                krakenflexDeviceId
                provider
                vehicleMake
                vehicleModel
                vehicleBatterySizeInKwh
                chargePointMake
                chargePointModel
                chargePointPowerInKw
                status
                suspended
                hasToken
                createdAt
            }
        }
        """
        variables = {'input': accountNumber}
        headers = {"Authorization": authToken}
        r = requests.post(url, json={'query': query, 'variables': variables, 'operationName': 'getData'}, headers=headers)
        formatted_json = json.loads(r.text)['data']
        print_json(formatted_json)
        return formatted_json
    except HTTPError as http_err:
        print(f'HTTP Error {http_err}')
    except Exception as err:
        print(f'Another error occurred: {err}')
        pass

def getTimesPlanned():
    graphQL = getObject()
    print()

def getTimesCompleted():
    graphQL = getObjectCompleted()
    print()

def getKraken():
    graphQL = getObjectAccount()
    print()

authToken = refreshToken(apikey, accountNumber)
getKraken()
getTimesPlanned()
getTimesCompleted()
