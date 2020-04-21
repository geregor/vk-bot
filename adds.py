import pymysql.cursorss

dhost = os.environ.get('TOKENH')
duser = os.environ.get('TOKENU')
dpassword = os.environ.get('TOKENP')
ddb = os.environ.get('TOKEND')
dcharset = os.environ.get('TOKENC')


def connect():
    connection = pymysql.connect(
        host=str(dhost),
        user=str(duser),
        password=str(dpassword),
        db=str(ddb),
        charset=str(dcharset),
        cursorclass=pymysql.cursors.DictCursor)
    return connection

# Level Score
# 1: 0
# 2: 125
# 3: 475
# 4: 1360
# 5: 4980
# 6: 11090
# 7: 23670
# 8: 48140
# 9: 95600
# 10: 200000

# 1. 5% к получаемым монетам с миссий 9,000,000,000 fivebonus
# 2. 10% к получаемому опыту с миссий 800,000,000 tenbonus
# 3. Время миссий сокращено на 2 минуты 70,000,000 time2mis
# 4. Уменьшает время работы заводов на 2 минуты 6,000,000 time2zav
# 5. С 5% шансом возвращает проигранные средства в казино 500,000 cashback
# 6. Время миссий сокращено на 7 минут 40,000 time2mis
# 7. Размер отряда увеличен до 30 человек 3,000 otryad
# 8. 15% к получаемым монетам с миссии 200 fivetybonus
# 9. 25% к получаемому опыту с миссий 10 twentyfivebonus
# 10. Время миссий сокращено на 12 минут 0 time2mis
