import bs4
import requests
import datetime
import urllib.parse
from config import token, chat_id

telegRq = "https://api.telegram.org/bot"


def post(text):
    t = urllib.parse.quote_plus(text)
    requests.get(telegRq+token+"/sendMessage?chat_id="+chat_id+"&text="+t)
