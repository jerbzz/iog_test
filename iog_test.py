#!/usr/bin/python3

import requests
import json
import re
from requests.models import HTTPError

url = "https://api.octopus.energy/v1/graphql/"
APIKeyPattern = re.compile('sk_live_[A-Za-z0-9]{24}?$')
accountNumberPattern = re.compile('A-[0-9A-F]{8}?$')

def refreshToken(apiKey,accountNumber):
    try:
        query = """
        mutation krakenTokenAuthentication($api: String!) {
        obtainKrakenToken(input: {APIKey: $api}) {
            token
        }
        }
        """
        variables = {'api': APIKey}
        r = requests.post(url, json={'query': query , 'variables': variables})
    except HTTPError as http_err:
        print(f'HTTP Error {http_err}')
    except Exception as err:
        print(f'Another error occurred: {err}')

    jsonResponse = json.loads(r.text)
    return jsonResponse['data']['obtainKrakenToken']['token']

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
        headers={"Authorization": authToken}
        r = requests.post(url, json={'query': query , 'variables': variables, 'operationName': 'getData'},headers=headers)
        return json.loads(r.text)['data']
    except HTTPError as http_err:
        print(f'HTTP Error {http_err}')
    except Exception as err:
        print(f'Another error occurred: {err}')

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
        headers={"Authorization": authToken}
        r = requests.post(url, json={'query': query , 'variables': variables, 'operationName': 'getData'},headers=headers)
        return json.loads(r.text)['data']
    except HTTPError as http_err:
        print(f'HTTP Error {http_err}')
    except Exception as err:
        print(f'Another error occurred: {err}')

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
        headers={"Authorization": authToken}
        r = requests.post(url, json={'query': query , 'variables': variables, 'operationName': 'getData'},headers=headers)
        return json.loads(r.text)['data']
    except HTTPError as http_err:
        print(f'HTTP Error {http_err}')
    except Exception as err:
        print(f'Another error occurred: {err}')

def getTimesPlanned():
    graphQL = getObject()
    print(graphQL)
    print()

def getTimesCompleted():
    graphQL = getObjectCompleted()
    print(graphQL)
    print()

def getKraken():
    graphQL = getObjectAccount()
    print(graphQL)
    print()

def getInput():
    global accountNumber
    accountNumber = input('Enter account number: ')
    accountMatch = accountNumberPattern.match(accountNumber)
    if accountMatch is None:
        raise SystemExit('Account number does not match expected pattern.')

    global APIKey
    APIKey = input('Enter API key: ')
    APIMatch = APIKeyPattern.match(APIKey)
    if APIMatch is None:
        raise SystemExit('API key does not match expected pattern.')

getInput()
authToken = refreshToken(accountNumber, APIKey)
getKraken()
getTimesPlanned()
getTimesCompleted()
