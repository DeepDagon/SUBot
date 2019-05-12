import sqlite3

#c.execute('''CREATE TABLE subscribers (id int auto_increment primary key, subid varchar)''')

def addToDataBase(id, date='', gameInfoTeam1='',gameInfoTeam2='',
                  gamePNG='', judges='', photos_url='',
                  place='', pointsTeam1='', pointsTeam2='',
                  teamName1='', teamName2='', video_attachment='', logo='', databasefile='games.db'):
    #Подключение к базе
    conn = sqlite3.connect(databasefile)

    #Создание курсора
    c = conn.cursor()

    #Добавление id в базу
    if c.execute("SELECT id FROM games WHERE id=?",(id,)).fetchall() == []:
        c.execute("INSERT INTO games VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",(id, date, gameInfoTeam1, gameInfoTeam2,
                                                 gamePNG, judges, photos_url, place,
                                                 pointsTeam1, pointsTeam2, teamName1,
                                                 teamName2, video_attachment, logo))
    else:
        if date != '':
            c.execute('UPDATE games SET date = ? WHERE id = ?', (date, id))
        if gameInfoTeam1 != '':
            c.execute('UPDATE games SET gameInfoTeam1 = ? WHERE id = ?', (gameInfoTeam1, id))
        if gameInfoTeam2 != '':
            c.execute('UPDATE games SET gameInfoTeam2 = ? WHERE id = ?', (gameInfoTeam2, id))
        if gamePNG != '':
            c.execute('UPDATE games SET gamePNG = ? WHERE id = ?', (gamePNG, id))
        if judges != '':
            c.execute('UPDATE games SET judges = ? WHERE id = ?', (judges, id))
        if photos_url != '':
            c.execute('UPDATE games SET photos_url = ? WHERE id = ?', (photos_url, id))
        if place != '':
            c.execute('UPDATE games SET place = ? WHERE id = ?', (place, id))
        if pointsTeam1 != '':
            c.execute('UPDATE games SET pointsTeam1 = ? WHERE id = ?', (pointsTeam1, id))
        if pointsTeam2 != '':
            c.execute('UPDATE games SET pointsTeam2 = ? WHERE id = ?', (pointsTeam2, id))
        if teamName1 != '':
            c.execute('UPDATE games SET teamName1 = ? WHERE id = ?', (teamName1, id))
        if teamName2 != '':
            c.execute('UPDATE games SET teamName2 = ? WHERE id = ?', (teamName2, id))
        if video_attachment != '':
            c.execute('UPDATE games SET video_attachment = ? WHERE id = ?', (video_attachment, id))
        if logo != '':
            c.execute('UPDATE games SET logo = ? WHERE id = ?', (logo, id))

    #Подтверждение отправки данных в базу
    conn.commit()

    #Завершение соединения
    c.close()
    conn.close()
    return id

def deleteNote(id, databasefile='games.db'):
    #Подключение к базе
    conn = sqlite3.connect(databasefile)
    id = -id
    #Создание курсора
    c = conn.cursor()
    #Удаление id из базы
    if c.execute("SELECT * FROM games WHERE id=?",(id,)).fetchall() != []:
        c.execute("DELETE FROM games WHERE id=?",(id,))

    #Подтверждение отправки данных в базу
    conn.commit()

    #Завершение соединения
    c.close()
    conn.close()
    return id


def getGameData(id, databasefile='games.db'):
    #Подключение к базе
    conn = sqlite3.connect(databasefile)
    #Создание курсора
    c = conn.cursor()
    #Удаление id из базы
    data =  c.execute("SELECT * FROM games WHERE id=?",(id,)).fetchall()
    if data != []:
       data = data[0]
    else:
        c.close()
        conn.close()
        return data

    data = {'id': data[0],
            'date': data[1],
            'gameInfoTeam1': data[2].split(';'),
            'gameInfoTeam2': data[3].split(';'),
            'gamePNG': data[4],
            'judges': data[5].split(';'),
            'photos_url': data[6].split(';'),
            'place': data[7],
            'pointsTeam1': data[8],
            'pointsTeam2': data[9],
            'teamName1': data[10],
            'teamName2': data[11],
            'video_attachment': data[12],
            'logo': data[13]
    }
    #Завершение соединения
    c.close()
    conn.close()

    return data


def getAllIds(coming=False, databasefile='games.db'):
    #Подключение к базе
    conn = sqlite3.connect(databasefile)

    #Создание курсора
    c = conn.cursor()
    #Удаление id из базы
    if coming:
        ids =  c.execute("SELECT id FROM games WHERE id<0").fetchall()
        ids = [-x[0] for x in ids]
    else:
        ids =  c.execute("SELECT id FROM games WHERE id>0").fetchall()
        ids = [x[0] for x in ids]


    #Завершение соединения
    c.close()
    conn.close()

    return ids
