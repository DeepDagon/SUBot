from dateutil import parser
from db import *
def sorting(L):
    splitup = L.split('-')
    return splitup[0], splitup[1], splitup[2], splitup[3], splitup[4]

def get_last(count=10):
    dates = {}
    for game in getAllIds():
        data = getGameData(id=game)
        date = data.get('date')
        date = date.replace('января','jan')
        date = date.replace('февраля','feb')
        date = date.replace('марта','mar')
        date = date.replace('апреля','apr')
        date = date.replace('мая','may')
        date = date.replace('июня','jun')
        date = date.replace('июля','jul')
        date = date.replace('августа','aug')
        date = date.replace('сентября','sept')
        date = date.replace('октября','oct')
        date = date.replace('ноября','nov')
        date = date.replace('декабря','dec')


        date = str(parser.parse(date)).replace(' ', '-').replace(':', '-')

        dates.update({date: game})
    keys = []
    for i in dates:
        keys.append(i)

    a = sorted(keys, key=sorting)

    last = []
    if count == 0:
        for x in a:
            last.append(dates[x])
    else:
        for x in a[-count:]:
            last.append(dates[x])

    return last
