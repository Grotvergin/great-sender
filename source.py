from common import *
from secret import *

BOT = telebot.TeleBot(TOKEN)
SERVICE = BuildService('sheets', 'v4')
SCAN = ('A2', 'L100')
COL_PHOTO = 3
COL_VIDEO = 4
COL_CIRCLE = 5
COL_VOICE = 6
COL_STICKER = 7
COL_LINK_URL = 8
COL_LINK_TEXT = 9
COL_ANIM = 10
COL_MSG = 11
