#!/usr/bin/python3.6
import json
import os

def get_conf(key):
    try:
        return os.environ[key.upper()]
    except:
        with open('../conf/config.json') as json_data_file:
            conf = json.load(json_data_file)
            return conf[key]
