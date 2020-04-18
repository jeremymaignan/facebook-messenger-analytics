#!/usr/local/bin/python3.7
# coding: utf8

import json
import os


def get_conf(key):
    try:
        return os.environ[key.upper()]
    except:
        with open('../config.json') as json_data_file:
            conf = json.load(json_data_file)
            return conf[key]

def open_file(filename):
    with open(filename) as content:
        return json.load(content)

def decode_str(str):
    if not str:
        return str
    return str.encode('latin1').decode('utf8')

def format_duration(duration_sec):
    m, s = divmod(duration_sec, 60)
    h, m = divmod(m, 60)
    d, h = divmod(h, 24)
    if d:
        return "{} Days {} Hours {} Minutes {} Secondes".format(int(d), int(h), int(m), int(s))
    elif h:
        return "{} Hours {} Minutes {} Secondes".format(int(h), int(m), int(s))
    elif m:
        return "{} Minutes {} Secondes".format(int(m), int(s))
    return "{} Secondes".format(int(s))
