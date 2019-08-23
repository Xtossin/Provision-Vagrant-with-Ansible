#!/usr/bin/python

import hashlib
import json
import requests

base_url = raw_input('Enter a url: ')
header_auth_token = raw_input("Enter authentication token header (tip call /auth to get) :")
auth_url = base_url + '/auth'
users_url = base_url + '/users'

req = requests.get(auth_url)
print(req.headers)


def endpoint_fails(base_url, max_attempts=3, **kwargs):
    attempts = 0
    while attempts < max_attempts:
        attempts += 1
        try:
            res = requests.get(base_url, **kwargs)
        except requests.exceptions.ConnectionError:
            continue
        if res.status_code == requests.codes.ok:
            return res

    raise requests.exceptions.HTTPError


def auth_token():
    try:
        res = endpoint_fails(auth_url)
    except requests.exceptions.HTTPError:
        return 1
    token = res.headers[header_auth_token]
    return token


def auth_checksum(token):
    encoded = (token + "/users").encode("utf-8")
    checksum = hashlib.sha256(encoded).hexdigest()
    return checksum


def user_ids(check_sum):
    res = endpoint_fails(users_url, headers={"X-Request-Checksum": check_sum})
    return res.content.decode()


def users():
    token = auth_token()
    check_sum = auth_checksum(token=token)
    users_b = user_ids(check_sum=check_sum)
    print(json.dumps(users_b.splitlines()))
    exit(0)


if __name__ == '__main__':
    users()
