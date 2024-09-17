# -*- coding: utf-8 -*-
# written by Paper

import requests
import subprocess
import time

def check_frpc_status(url):
    global result
    try:
        # check frpc.service status
        headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        check_result = subprocess.check_output(["systemctl", "is-active", "frpc.service"])
        status = check_result.decode().strip()
        if status == "active": # frpc.service is active
            try:
                response = requests.get(url, headers=headers, timeout=5)
                if response.status_code == 200:
                    result = "successful"
                else:
                    result = "connect is failed"
            except requests.exceptions.RequestException: # Unable to access website
                result = "request error"
        else: # frpc.service is not active
            result = "frpc.service is not active"
    except subprocess.CalledProcessError:
        result = "check error"

def start_frpc_service():
    try:
        subprocess.check_call(["systemctl", "start", "frpc.service"])
    except subprocess.CalledProcessError:
        print("start error")

if __name__ == "__main__":
    url = "https://www.simple-paper.us.kg"
    while True:
        check_frpc_status(url)
        if result == "successful":
            print("successful")
            break
        elif result == "frpc.service is not active":
            print('frpc.service is not active')
            start_frpc_service()
            time.sleep(30)
            continue
        elif result == "request error" or result == "check error":
            print(result)
            start_frpc_service()
            time.sleep(30)
            continue