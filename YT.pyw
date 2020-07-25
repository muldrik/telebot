from config import api_key, token, chat_id
from YTChannels import channels
from googleapiclient.discovery import build
from telegramHandler import post

yt = build('youtube', 'v3', developerKey=api_key)

f = open('C:/Users/muldr/PycharmProjects/TelegramBotV1/channelauto.txt', 'r')
logged_channels = f.read()
f.close()

f = open('C:/Users/muldr/PycharmProjects/TelegramBotV1/posted.txt', 'r')
ids = f.read()
f.close()
new_ids = []


# get new video ids from the list of channels
for channel in channels:
    uploadsId = channel[1]
    rq = yt.playlistItems().list(part='contentDetails', playlistId=uploadsId)
    response = rq.execute()
    if channel[1] not in logged_channels:
        f = open('C:/Users/muldr/PycharmProjects/TelegramBotV1/posted.txt', 'a')
        for vid in response['items']:
            new_id = vid['contentDetails']['videoId']
            f.write(new_id+'\n')
        f.close()
        f = open('C:/Users/muldr/PycharmProjects/TelegramBotV1/channelauto.txt', 'a')
        f.write(channel[1]+'\n')
        f.close()
    else:
        for vid in response['items']:
            new_id = vid['contentDetails']['videoId']
            if ids.find(new_id) == -1:
                new_ids.append(new_id+'\n')


# Update list of ids
f = open('C:/Users/muldr/PycharmProjects/TelegramBotV1/posted.txt', 'a')
for new_id in new_ids:
    f.write(new_id)
f.close()

# post new vids
YTbase = "https://www.youtube.com/watch?v="
for new_id in new_ids:
    post(YTbase+new_id)
