from common import *
from secret import *

BOT = telebot.TeleBot(TOKEN)
SERVICE = BuildService('sheets', 'v4')
PATTERN = r'https://drive\.google\.com/file/d/([^/]+)/view\?usp=drive_link'