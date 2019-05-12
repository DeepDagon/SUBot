import vk_api
import yaml
import os
import requests
from db import *
from config import *

vk_session1 = vk_api.VkApi(token= user_token)
try:
    vk_session1.auth()
except vk_api.AuthError as error_msg:
    print(error_msg)

vk1 = vk_session1.get_api()


def GetVideoUrl(url):

    data = vk1.video.save(link=url, group_id= int(group_id))
    requests.get(data['upload_url'])

    video = "video{}_{}".format(data['owner_id'], data["video_id"])

    return video

def writeUrlVideo(id, video):
    addToDataBase(id=id, video_attachment=video)


def checkUrlsVideo(id):
    data = getGameData(id)

    video_attachment = data.get('video_attachment')

    if video_attachment != None:
        return True
    else:
        return False

# ids = os.listdir('games/')
# for id in sorted(ids):
#     path = 'games/' + str(id)
#
#     current = checkUrlsVideo(path + '/info.yaml')
#     print(str(id) + '   ' + str(current))
#
#     if current == False:
#         with open(path + '/info.yaml', 'r') as stream:
#             data = yaml.load(stream)
#         url = data.get('video')
#         video_url = GetVideoUrl(url)
#         writeUrlVideo(path + '/info.yaml', video_url)
