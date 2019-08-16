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
import os
import boto3
import json
import sys
import time
import requests
import datetime

#username = os.environ.get("username", None)
#password = os.environ.get("password", None)
#customername = os.environ.get("customername", None)
#url = os.environ.get("urlname", None)
#s3_bucket = os.environ.get("TargetS3Bucket", None)
#csv_file_name = '/tmp/alert_list.csv'
yes=True
def config():
    global username
    global password
    global customername
    global url
    global s3_bucket
    global csv_file_name
    global rl_settings
    username = os.environ['username']
    password = os.environ['password']
    customername = os.environ['customername']
    url = os.environ['url']
    s3_bucket = os.environ['TargetS3Bucket']
    csv_file_name = '/tmp/alert_list.csv'
    rl_settings = {}
    rl_settings['username'] = username
    rl_settings['password'] = password
    rl_settings['customerName'] = customername
    rl_settings['apiBase'] = url
    rl_settings['jwt'] = None
    print(rl_settings['apiBase'])
# --End parse command line arguments-- #
# --Main-- #
# Get login details worked out
#rl_settings = rl_lib_general.rl_login_get(username, password, customername, url)


def upload_csv_file(filename, key):
    """Upload generated file to S3 Bucket"""
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(s3_bucket)
    bucket.upload_file(filename, key)


def create_csv_file(csv_file_name,rl_settings):
  print(rl_settings['apiBase'])
  rl_settings = rl_lib_api.rl_jwt_get(rl_settings)
  print(rl_settings)
  rl_settings, response_package = rl_lib_api.alltime_alert_list_get(rl_settings)
  alertdata = response_package['data']
  print(alertdata)
  masterlist=[]
  for each in alertdata:
    list=[]
    list.append(each['status'])
    list.append(each['policy']['name'])
    list.append(each['resource']['name'])
    list.append(each['resource']['accountId'])
    list.append(each['resource']['region'])
    list.append(each['resource']['account'])
    list.append(each['policy']['severity'])
    try:
        each['resource']['id']
    except KeyError:
        list.append('None')
    else:
      list.append(each['resource']['id'])
    try:
        each['id']
    except KeyError:
        list.append('None')
    else:
        list.append(each['id'])
    try:
        each['alertTime']
    except KeyError:
        list.append('None')
    else:
        try:
            formattedtime = datetime.datetime.fromtimestamp(each['alertTime']/1000).strftime('%Y-%m-%d %H:%M:%S')
        except ValueError:
            list.append('None')
        else:
            list.append(formattedtime)
    masterlist.append(list)


  with open(csv_file_name, "w") as f:
  	writer = csv.writer(f)
  	writer.writerow(["Status", "Policy Name", "Resource Name", "Account ID", "Region", "Account Name", "Severity", "Resource ID", "Alert ID", "Alert Time"])
  	writer.writerows(masterlist)

def main(event, context):
  get_config = config()
  result = create_csv_file(csv_file_name,rl_settings)
  upload = upload_csv_file(csv_file_name, 'alertlist-%s.csv' % time.strftime("%d-%m-%Y"))


