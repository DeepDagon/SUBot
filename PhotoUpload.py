import vk_api
import yaml
import os
import shutil
from db import *
from config import *

vk_session = vk_api.VkApi(token=token)
vk = vk_session.get_api()

upload = vk_api.VkUpload(vk_session)

def GetPhotoUrl(path):

    path = [path[i::7] for i in range(7) if path[i::7] != []]

    photo_url = []

    for i in path:
        photo_url += upload.photo_messages(i)

    photos = ["photo{}_{}".format(photo_url[x[0]]['owner_id'], photo_url[x[0]]["id"]) for x in enumerate(photo_url)]

    return photos

def writeUrl(id, photos, isGamePNG=False):
    if isGamePNG:
        addToDataBase(id=id, gamePNG=photos[0])
    else:
        addToDataBase(id=id, photos_url=';'.join(photos))

def checkUrls(id, isGamePNG=False):
    data = getGameData(id)
    if isGamePNG:
        gamePNG = data.get('gamePNG')
        if gamePNG != None:
            return True
        else:
            return False
    else:
        photos = data.get('photos_url')
        if photos != []:
            return True
        else:
            return False

def delPhotos(id, gamePNG=False):
    if gamePNG:
        uploaded = checkUrls(id, isGamePNG=True)
        if uploaded:
            os.remove('src/temp/' + str(id) + '/game.png')
    else:
        uploaded = checkUrls(id)
        if uploaded:
            shutil.rmtree('src/temp/' + str(id) +'/photos')
