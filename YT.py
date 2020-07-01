from config import api_key, token, chat_id
from YTChannels import channels
from googleapiclient.discovery import build
from datetime import datetime
import urllib.parse, requests

telegRq = "https://telegg.ru/orig/bot"
def post(text):
    t = urllib.parse.quote_plus(text)
    requests.get(telegRq+token+"/sendMessage?chat_id="+chat_id+"&text="+t)

yt = build('youtube', 'v3', developerKey=api_key)

f = open('channelauto.txt', 'r')
logged_channels = f.read()
f.close()

f = open('posted.txt', 'r')
ids = f.read()
f.close()
new_ids = []

time_now = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")



#get new video ids from the list of channels
for channel in channels:
    if (channel.find('user')!=-1):
        username = channel[channel.find('user')+5:]
        rq = yt.channels().list(part='contentDetails', forUsername=username)
    else:
        channelId = channel[channel.find('channel')+8:]
        rq = yt.channels().list(part='contentDetails', id=channelId)
    response = rq.execute()
    uploadsId = response['items'][0]['contentDetails']['relatedPlaylists']['uploads']
    print(uploadsId)
    rq = yt.playlistItems().list(part='contentDetails', playlistId=uploadsId)
    response = rq.execute()
    if channel not in logged_channels:
        f = open('posted.txt', 'a')
        for vid in response['items']:
            new_id = vid['contentDetails']['videoId']
            f.write(new_id+'\n')
        f.close()
        f = open('channelauto.txt', 'a')
        f.write(channel+'\n')
        f.close()
    else:
        for vid in response['items']:
            new_id = vid['contentDetails']['videoId']
            if ids.find(new_id) == -1:
                new_ids.append(new_id+'\n')


#Update list of ids
f = open('posted.txt', 'a')
for new_id in new_ids:
    f.write(new_id)
f.close()

#post new vids
YTbase = "https://www.youtube.com/watch?v="
for new_id in new_ids:
    post(YTbase+new_id)
