#!/usr/bin/env python
from __future__ import print_function
try:
    input = raw_input
except NameError:
    pass
import argparse
import rl_lib_api
import rl_lib_general
import csv

# --Execution Block-- #
# --Parse command line arguments-- #
parser = argparse.ArgumentParser(prog='rltoolbox')

parser.add_argument(
    '-u',
    '--username',
    type=str,
    help='*Required if no settings file has been created* - Redlock API UserName that you want to set to access your Redlock account.')

parser.add_argument(
    '-p',
    '--password',
    type=str,
    help='*Required if no settings file has been created* - Redlock API password that you want to set to access your Redlock account.')

parser.add_argument(
    '-c',
    '--customername',
    type=str,
    help='*Required if no settings file has been created* - Name of the Redlock account to be used.')

parser.add_argument(
    '-url',
    '--uiurl',
    type=str,
    help='*Required if no settings file has been created* - Base URL used in the UI for connecting to Redlock.  '
         'Formatted as app.redlock.io or app2.redlock.io or app.eu.redlock.io, etc.')

parser.add_argument(
    '-y',
    '--yes',
    action='store_true',
    help='(Optional) - Override user input for verification (auto answer for yes).')

args = parser.parse_args()
# --End parse command line arguments-- #
# --Main-- #
# Get login details worked out
rl_settings = rl_lib_general.rl_login_get(args.username, args.password, args.customername, args.uiurl)

# Verification (override with -y)
if not args.yes:
    print()
    print('This action will be done against the customer account name of "' + rl_settings['customerName'] + '".')
    verification_response = str(input('Is this correct (y or yes to continue)?'))
    continue_response = {'yes', 'y'}
    print()
    if verification_response not in continue_response:
        rl_lib_general.rl_exit_error(400, 'Verification failed due to user response.  Exiting...')

# Sort out API Login
print('API - Getting authentication token...', end='')

rl_settings = rl_lib_api.rl_jwt_get(rl_settings)
rl_settings, response_package = rl_lib_api.api_alert_list_get(rl_settings)
alertdata = response_package['data']
masterlist=[]
for each in alertdata:
  list=[]
  list.append(each['status'])
  list.append(each['policy']['name'])
  try:
      each['resource']['id']
  except KeyError:
      list.append('None')
  else:
      list.append(each['resource']['id'])
  list.append(each['resource']['name'])
  list.append(each['resource']['accountId'])
  list.append(each['resource']['region'])
  masterlist.append(list)


with open("alerts.csv", "w") as f:
	writer = csv.writer(f)
	writer.writerow(["Status", "Policy Name", "Resource ID", "Resource Name", "Account ID", "Region"])
	writer.writerows(masterlist)

print('Done.')
