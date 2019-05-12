from PIL import Image, ImageDraw, ImageFont
from db import getGameData

def drawInfo(id):
    data = getGameData(id)

    if int(data.get('pointsTeam1')) > int(data.get('pointsTeam2')):
        template = Image.open('src/wl.png')
    else:
        template = Image.open('src/lw.png')

    if data.get('teamName1') == 'Южный Урал':
        logo1 = Image.open('src/logos/big_logo_yu_orsk_2016.png')
        logo2 = Image.open(data.get('logo'))
        template.paste(logo1, (200,295), logo1)
        try:
            template.paste(logo2, (850,295), logo2)
        except:
            template.paste(logo2, (850,295))
    else:
        logo1 = Image.open(data.get('logo'))
        logo2 = Image.open('src/logos/big_logo_yu_orsk_2016.png')
        template.paste(logo2, (850,295), logo2)
        try:
            template.paste(logo1, (200,295), logo1)
        except:
            template.paste(logo1, (200,295))


    draw = ImageDraw.Draw(template)

    fnt_date = ImageFont.truetype('src/exo2bold.otf', 20)
    date = data.get('date')
    w, h = draw.textsize(text=date, font=fnt_date)
    draw.text(((1200-w)/2, 20), date, fill='black', font=fnt_date)

    fnt_place = ImageFont.truetype('src/exo2bold.otf', 26)
    place = data.get('place')
    w, h = draw.textsize(text=place, font=fnt_place)
    draw.text(((1200-w)/2, 90), place, fill='black', font=fnt_place)

    fnt_judge = ImageFont.truetype('src/Exo2.otf', 16)
    judges = data.get('judges')
    k = 0
    for i in judges:
        w, h = draw.textsize(text=i, font=fnt_judge)
        draw.text((1200/4*k + 100, 200), i, fill='black', font=fnt_judge)
        k += 1

    fnt_points = ImageFont.truetype('src/Exo2.otf', 160)
    points1 = data.get('pointsTeam1')
    w, h = draw.textsize(text=points1, font=fnt_points)
    draw.text(((1200-w)/2 - 70, 300), points1, fill='white', font=fnt_points)

    points2 = data.get('pointsTeam2')
    w, h = draw.textsize(text=points2, font=fnt_points)
    draw.text(((1200-w)/2 + 70, 300), points2, fill='white', font=fnt_points)

    fnt_teamName = ImageFont.truetype('src/exo2bold.otf', 34)
    teamName1 = data.get('teamName1')
    w, h = draw.textsize(text=teamName1, font=fnt_teamName)
    draw.text((600-w-50, 250), teamName1, fill='white', font=fnt_teamName)

    teamName2 = data.get('teamName2')
    w, h = draw.textsize(text=teamName2, font=fnt_teamName)
    draw.text((600+50, 250), teamName2, fill='white', font=fnt_teamName)

    fnt_teamInfo = ImageFont.truetype('src/Exo2.otf', 25)
    teamInfo1 = data.get('gameInfoTeam1')
    y = 500
    for x in teamInfo1:
        w, h = draw.textsize(text=x, font=fnt_teamInfo)
        draw.text(((550-w)/2, y), x, fill='white', font=fnt_teamInfo)
        y+=30

    teamInfo2 = data.get('gameInfoTeam2')
    y = 500

    for x in teamInfo2:
        w, h = draw.textsize(text=x, font=fnt_teamInfo)
        draw.text((1200 - (550+w)/2, y), x, fill='white', font=fnt_teamInfo)
        y+=30

    path = 'src/temp/' + str(id) + '/game.png'
    template.save(path)
    return path
