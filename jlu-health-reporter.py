#!/usr/bin/env python3
USERS = [('daim2213', 'password')]
# USERNAME and USERPASS are deprecated now for multi-user support
USERNAME = 'daim2213'
USERPASS = 'password'

MAX_RETRY = 1
RETRY_INTERVAL = 20
TRANSACTION = 'JLDX_BK_XNYQSB'  # 'JLDX_YJS_XNYQSB'git
CLOCKIN = 'BKSMRDK'  # 本科生每日打卡
DEBUG = 0  # +1s

import re
from sys import argv
import json
from time import time, sleep
import urllib3
import requests
import logging
from logging import debug, info, warning, error, critical
import random

logging.basicConfig(level=logging.INFO - 10 * DEBUG, format='%(asctime)s %(levelname)s %(message)s')
warning('Started.')
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
if USERS is None: USERS = [(USERNAME, USERPASS)]

def login(s, username, password):
    info('User: ' + username)
    info('Authenticating...')

    s.headers.update({'Referer': 'https://ehall.jlu.edu.cn/'})
    s.verify = False

    r = s.get('https://ehall.jlu.edu.cn/jlu_portal/login')
    pid = re.search('(?<=name="pid" value=")[a-z0-9]{8}', r.text)[0]
    debug('PID: ' + pid)

    postPayload = {'username': username, 'password': password, 'pid': pid}
    r = s.post('https://ehall.jlu.edu.cn/sso/login', data=postPayload)


# type 早上：fieldZtw
# 中午：fieldZhongtw
# 傍晚：fieldWantw
# 晚上：unkown
def clockIn(session, type):
    info('Requesting form...')
    r = session.get('https://ehall.jlu.edu.cn/infoplus/form/' + CLOCKIN + '/start')
    csrfToken = re.search('(?<=csrfToken" content=").{32}', r.text)[0]
    debug('CSRF: ' + csrfToken)

    postPayload = {'idc': CLOCKIN, 'csrfToken': csrfToken}
    r = session.post('https://ehall.jlu.edu.cn/infoplus/interface/start', data=postPayload)
    sid = re.search('(?<=form/)\\d*(?=/render)', r.text)[0]
    debug('Step ID: ' + sid)

    postPayload = {'stepId': sid, 'csrfToken': csrfToken}
    r = session.post('https://ehall.jlu.edu.cn/infoplus/interface/render', data=postPayload)
    data = json.loads(r.content)['entities'][0]
    payload_1 = data['data']

    if type != 'wanQ': payload_1[type] = '1'

    payload_1 = json.dumps(payload_1)
    debug('DATA: ' + payload_1)
    payload_2 = ','.join(data['fields'].keys())
    debug('FIELDS: ' + payload_2)

    info('Submitting form...')

    rand = random.randint(10000000000000000, 90000000000000000) / 10000000000000

    postPayload = {
        'actionId': 1,
        'formData': payload_1,
        'nextUsers': '{}',
        'stepId': sid,
        'rand': rand,
        'timestamp': int(time()),
        'boundFields': payload_2,
        'csrfToken': csrfToken
    }
    r = session.post('https://ehall.jlu.edu.cn/infoplus/interface/doAction', data=postPayload)
    debug(r.text)
    if json.loads(r.content)['ecode'] != 'SUCCEED':
        raise Exception('The server returned a non-successful status.')

    info('Success!')

def health(s):
    info('Requesting form...')
    r = s.get('https://ehall.jlu.edu.cn/infoplus/form/' + TRANSACTION + '/start')
    csrfToken = re.search('(?<=csrfToken" content=").{32}', r.text)[0]
    debug('CSRF: ' + csrfToken)

    postPayload = {'idc': TRANSACTION, 'csrfToken': csrfToken}
    r = s.post('https://ehall.jlu.edu.cn/infoplus/interface/start', data=postPayload)
    sid = re.search('(?<=form/)\\d*(?=/render)', r.text)[0]
    debug('Step ID: ' + sid)

    postPayload = {'stepId': sid, 'csrfToken': csrfToken}
    r = s.post('https://ehall.jlu.edu.cn/infoplus/interface/render', data=postPayload)
    data = json.loads(r.content)['entities'][0]
    payload_1 = data['data']
    payload_1['fieldCNS'] = True
    payload_1 = json.dumps(payload_1)
    debug('DATA: ' + payload_1)
    payload_2 = ','.join(data['fields'].keys())
    debug('FIELDS: ' + payload_2)

    info('Submitting form...')
    postPayload = {
        'actionId': 1,
        'formData': payload_1,
        'nextUsers': '{}',
        'stepId': sid,
        'timestamp': int(time()),
        'boundFields': payload_2,
        'csrfToken': csrfToken
    }
    r = s.post('https://ehall.jlu.edu.cn/infoplus/interface/doAction', data=postPayload)
    debug(r.text)

    if json.loads(r.content)['ecode'] != 'SUCCEED':
        raise Exception('The server returned a non-successful status.')

    info('Success!')


# main_loop
for username, password in USERS:
    for tries in range(0, MAX_RETRY):
        try:
            #登录
            s = requests.Session()
            login(s,username,password)
            #填表
            if argv[1] == '-m' or argv[1] == '--morning':
                clockIn(s, 'fieldZtw')
            elif argv[1] == '-n' or argv[1] == '--noon':
                clockIn(s, 'fieldZHongtw')
            elif argv[1] == '-a' or argv[1] == '--afternoon':
                clockIn(s, 'fieldWantw')
            elif argv[1] == '-e' or argv[1] == '--evening':
                clockIn(s, 'wanQ')
            elif argv[1] == '-h' or argv[1] == '--health':
                health(s)
            break
        except Exception as e:
            warning(e)
            if tries + 1 == MAX_RETRY:
                error('Failed too many times! Skipping...')
                break
            error('Unknown error occured, retrying...')
            sleep(RETRY_INTERVAL)
