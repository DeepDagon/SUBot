# -*- coding: utf-8 -*-
import os
import requests, bs4
import re
from db import *
from drawInfo import drawInfo
from PhotoUpload import *
from VideoUpload import *
from urllib.parse import unquote

removal = [92, 93, 211]

# IDEA: НУЖНО ПРИ УСТАНОВКИ СРАЗУ СОЗДАВАТЬ ВСЕ ПАПКИ И КАЧАТЬ ЛОГОТИП НУЖНОЙ КОМАНДЫ
def findLogo(parser):
    if findTeam(parser, 0) == 'Южный Урал':
        url = parser.find('img', {'alt': findTeam(parser, 1)}).get('src')
    else:
        url = parser.find('img', {'alt': findTeam(parser, 0)}).get('src')

    url = 'http://www.orsk-hockey.ru/' + url
    path = 'src/logos/' + url.split('/')[-1:][0].replace('jpg', 'png')
    path = unquote(path)
    if not os.path.exists(path):
        r = requests.get(url, allow_redirects=True)
        open(path, 'wb').write(r.content)
    return path

def findDate(parser):
    return parser.find('h6', {'class': 'PageSubHeading BorderBottom GameDate'}).text.strip()

def findPlace(parser):
    return parser.find('h5', {'class': 'PageSubHeading GamePlace'}).text.strip()

def findTeam(parser, TeamId):
    return parser.findAll('h3', {'class': 'TeamTitle'})[TeamId].text.strip()

def NotFound(parser):
    if parser.find('h1') != None and parser.find('h1').text == 'Страница не найдена':
        return True

def Coming(parser, id):
    exists = False
    coming_ids = getAllIds(coming=True)
    for x in coming_ids:
        if x == id:
            exists = True

    if (TeamPoints(parser, 0) == '-') and (id not in removal):
        date = findDate(parser)
        place = findPlace(parser)
        team1 = findTeam(parser, 0)
        team2 = findTeam(parser, 1)

        if not(exists):
            addToDataBase(id=-id, date=date, place=place, teamName1=team1, teamName2=team2)
        return True

    elif (TeamPoints(parser, 0) != '-') and exists:
        deleteNote(id)
        return False


def findGameInfo(parser, TeamId):
    return parser.findAll('div', {'class': 'GameInfo'})[TeamId].text.replace('\n\n            ', '').split('\n')[:-2]

def findJudge(parser):
    judges = []
    parsed = parser.findAll('td', align='center')
    for x in range(0,len(parsed)):
        judges.append(parsed[x].text.strip())
    return judges

def TeamPoints(parser, TeamId):
    return parser.findAll('div', {'class': 'TeamCount'})[TeamId].text.strip()


def findPhotos(parser, id):
    photos = parser.findAll('div', {'class': 'popup-gallery'})
    photos_to_upload = []
    if photos != []:
        photos_path = 'src/temp/' + str(id) + '/photos'
        if not os.path.exists(photos_path):
            os.makedirs(photos_path)


        for photo in photos[0:10]:
            url = photo.find('a').get('href')
            url = 'http://www.orsk-hockey.ru' + url
            photo_path = photos_path + '/' + url.split('/')[-1:][0]
            if not os.path.exists(photo_path):
                r = requests.get(url, allow_redirects=True)
                open(photo_path, 'wb').write(r.content)
            photos_to_upload.append(photo_path)
        urls = GetPhotoUrl(photos_to_upload)
        writeUrl(id, photos=urls, isGamePNG=False)
        delPhotos(id)
        return True
    else:
        return False

def findVideo(parser, id):
    video = parser.find('iframe')

    if video != None:
        video = video.get('src')
        video_url = 'https://youtu.be/' + video.split('/')[-1:][0]
        url = GetVideoUrl(video_url)
        return writeUrlVideo(id, url)
    else:
        return None

def checkComing():
    released = []
    comingIds = getAllIds(coming= True)
    for id in comingIds:
        site = requests.get('http://www.orsk-hockey.ru/games/' + str(id))
        parser = bs4.BeautifulSoup(site.text, 'html.parser')

        if (TeamPoints(parser, 0) != '-'):
            deleteNote(id)
            released.append(id)

    return released


def parse_archive(id):

    site = requests.get('http://www.orsk-hockey.ru/games/' + str(id))
    parser = bs4.BeautifulSoup(site.text, 'html.parser')

    if NotFound(parser):
        return '404'

    if Coming(parser, id):
        return 'coming'

    path = 'src/temp/' + str(id)
    if not os.path.exists(path) and id not in removal:
        os.makedirs(path)

    logo_path = findLogo(parser)

    gameInfoTeam1 = findGameInfo(parser, 0)
    gameInfoTeam2 = findGameInfo(parser, 1)

    judges = findJudge(parser)

    pointsTeam1 = TeamPoints(parser, 0)
    pointsTeam2 = TeamPoints(parser, 1)

    teamName1 = findTeam(parser, 0)
    teamName2 = findTeam(parser, 1)

    date = findDate(parser)
    place = findPlace(parser)
    findPhotos(parser, id)

    video = findVideo(parser, id)

    data = {'id': id,
            'logo': logo_path,
            'gameInfoTeam1': gameInfoTeam1,
            'gameInfoTeam2': gameInfoTeam2,
            'judges': judges,
            'teamName1': teamName1,
            'teamName2': teamName2,
            'date': date,
            'place': place,
            'pointsTeam1': pointsTeam1,
            'pointsTeam2': pointsTeam2,
            }
    if id not in removal:
        addToDataBase(id=id, logo= logo_path, gameInfoTeam1= ';'.join(gameInfoTeam1),
                      gameInfoTeam2= ';'.join(gameInfoTeam2), judges= ';'.join(judges),
                      teamName1=teamName1, teamName2=teamName2,
                      date= date, place= place,
                      pointsTeam1= pointsTeam1, pointsTeam2= pointsTeam2)
        path = [drawInfo(id)]
        urls = GetPhotoUrl(path)
        writeUrl(id, photos=urls, isGamePNG=True)
        delPhotos(id, gamePNG=True)
        os.rmdir('src/temp/' + str(id))
        return True
