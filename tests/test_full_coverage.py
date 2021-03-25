import datetime as dt
import subprocess
import threading
import time
import signal
import pathlib
import socket

import requests
import pytest

from soliddisco.utils import Connection


_SERVER_ADDRESS = '127.0.0.1', 5666

_USER_1 = 21
_TIMESTAMP_1 = int(dt.datetime(2019, 10, 25, 15, 12, 5, 228000).timestamp())
_THOUGHT_1 = "I'm 21"

_WEBSERVER_ADDRESS = '127.0.0.1', 8666
_WEBSERVER_URL = 'http://localhost:8666'
_DATA_DIR = pathlib.Path(__file__).absolute().parent.parent / 'data'

_PORT = 6666

def test_cli_ser(tmp_path):
    host, port = _SERVER_ADDRESS
    cmd = ['python', '-m', 'soliddisco', 'server', 'run_server',
           f'{host}:{port}', str(tmp_path)]
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, )

    def run_server():
        process.communicate()
    thread = threading.Thread(target=run_server)
    thread.start()
    time.sleep(1)

    host, port = _SERVER_ADDRESS
    cmd = ['python', '-m', 'soliddisco', 'client', 'upload_thought',
           f'{host}:{port}', str(_USER_1), _THOUGHT_1]
    process_c = subprocess.Popen(cmd, stdout=subprocess.PIPE, )
    stdout_c, _ = process_c.communicate()
    assert b'done' in stdout_c.lower()

    process.send_signal(signal.SIGINT)
    thread.join()
    # thought_path_1 = _get_path(tmp_path, _USER_1, _TIMESTAMP_1)
    # assert thought_path_1.read_text() == _THOUGHT_1


def test_error():
    cmd = ['python', '-m', 'soliddisco', 'client', 'error']
    process_c = subprocess.Popen(cmd, stdout=subprocess.PIPE, )
    stdout_c, _ = process_c.communicate()
    assert b'wrong' in stdout_c.lower()
    cmd = ['python', '-m', 'soliddisco', '-q', 'client', 'error']
    process_c = subprocess.Popen(cmd, stdout=subprocess.PIPE, )
    stdout_c, _ = process_c.communicate()
    assert stdout_c.lower() in b''
    cmd = ['python', '-m', 'soliddisco', '-t', 'client', 'error']
    process_c = subprocess.Popen(cmd, stdout=subprocess.PIPE, )
    stdout_c, _ = process_c.communicate()
    assert b'wrong' in stdout_c.lower()


def test_web():
    host, port = _WEBSERVER_ADDRESS
    cmd = ['python', '-m', 'soliddisco', 'website', 'run_webserver',
           f'{host}:{port}', str(_DATA_DIR)]
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, )
    def run_server():
        process.communicate()
    thread = threading.Thread(target=run_server)
    thread.start()
    time.sleep(1)
    response = requests.get(f'{_WEBSERVER_URL}')

    for user_dir in _DATA_DIR.iterdir():
        response = requests.get(f'{_WEBSERVER_URL}/users/{user_dir.name}')
        for thought_file in user_dir.iterdir():
            dtt = dt.datetime.strptime(thought_file.stem, '%Y-%m-%d_%H-%M-%S')
            assert f'User {user_dir.name}' in response.text
            assert f'{dtt:%Y-%m-%d %H:%M:%S}' in response.text
            thought_file.read_text() in response.text
    process.send_signal(signal.SIGINT)
    thread.join()
