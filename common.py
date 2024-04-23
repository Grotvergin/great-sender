import telebot
from socket import gaierror
from ssl import SSLEOFError
from datetime import datetime, timedelta, date
from colorama import Fore, Style, init
import traceback
from typing import Union, Callable, Any, List, Dict, Generator
from threading import Thread
from googleapiclient.errors import HttpError
import httplib2
import googleapiclient.discovery
import time
import random
from google.oauth2 import service_account
from googleapiclient.discovery import build
from secret import *


SLEEP_GOOGLE = 20
MAX_ROW = 1000
init()
random.seed()
CREDS = service_account.Credentials.from_service_account_file('keys.json', scopes=['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive.readonly'])


def UploadRow(start: str, finish: str, data: list[str], sheet_name: str, sheet_id: str, service: googleapiclient.discovery.Resource) -> None:
    Stamp(f'Trying to upload data to sheet {sheet_name}', 'i')
    try:
        res = service.spreadsheets().values().update(spreadsheetId=sheet_id,
                                                 range=f'{sheet_name}!{start}:{finish}',
                                                 valueInputOption='USER_ENTERED', body={'values': [data]}).execute()
    except (TimeoutError, httplib2.error.ServerNotFoundError, gaierror, HttpError, SSLEOFError) as err:
        Stamp(f'Status = {err} on uploading data to sheet {sheet_name}', 'e')
    else:
        Stamp(f"On uploading: {res.get('updatedRows')} rows in range {res.get('updatedRange')}", 's')


def BuildService(serv_type: str, version: str) -> googleapiclient.discovery.Resource:
    Stamp(f'Trying to build {serv_type} service', 'i')
    try:
        service = build(f'{serv_type}', f'{version}', credentials=CREDS)
    except (HttpError, TimeoutError, httplib2.error.ServerNotFoundError, gaierror, SSLEOFError) as err:
        Stamp(f'Status = {err} on building {serv_type} service', 'e')
        Sleep(SLEEP_GOOGLE)
        BuildService()
    else:
        Stamp(f'Built {serv_type} service successfully', 's')
        return service


def Sleep(timer: int, ratio: float = 0.0) -> None:
    rand_time = random.randint(int((1 - ratio) * timer), int((1 + ratio) * timer))
    Stamp(f'Sleeping {rand_time} seconds', 'l')
    time.sleep(rand_time)


def Stamp(message: str, level: str) -> None:
    time_stamp = datetime.now().strftime('[%m-%d|%H:%M:%S]')
    match level:
        case 'i':
            print(Fore.LIGHTBLUE_EX + time_stamp + '[INF] ' + message + '.' + Style.RESET_ALL)
        case 'w':
            print(Fore.LIGHTMAGENTA_EX + time_stamp + '[WAR] ' + message + '!' + Style.RESET_ALL)
        case 's':
            print(Fore.LIGHTGREEN_EX + time_stamp + '[SUC] ' + message + '.' + Style.RESET_ALL)
        case 'e':
            print(Fore.RED + time_stamp + '[ERR] ' + message + '!!!' + Style.RESET_ALL)
        case 'l':
            print(Fore.WHITE + time_stamp + '[SLE] ' + message + '...' + Style.RESET_ALL)
        case 'b':
            print(Fore.LIGHTYELLOW_EX + time_stamp + '[BOR] ' + message + '.' + Style.RESET_ALL)
        case _:
            print(Fore.WHITE + time_stamp + '[UNK] ' + message + '?' + Style.RESET_ALL)


def GetSector(start: str, finish: str, service: googleapiclient.discovery.Resource, sheet_name: str, sheet_id: str) -> list:
    Stamp(f'Trying to get sector from {start} to {finish} from sheet {sheet_name}', 'i')
    try:
        res = service.spreadsheets().values().get(spreadsheetId=sheet_id, range=f'{sheet_name}!{start}:{finish}').execute().get('values', [])
    except (TimeoutError, httplib2.error.ServerNotFoundError, gaierror, HttpError, SSLEOFError) as err:
        Stamp(f'Status = {err} on getting sector from {start} to {finish} from sheet {sheet_name}', 'e')
        Sleep(SLEEP_GOOGLE)
        res = GetSector(start, finish, service, sheet_name, sheet_id)
    else:
        if not res:
            Stamp(f'No elements in sector from {start} to {finish} sheet {sheet_name} found', 'w')
        else:
            Stamp(f'Found {len(res)} rows from sector from {start} to {finish} sheet {sheet_name}', 's')
    return res
