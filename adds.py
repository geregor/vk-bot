import pymysql.cursors

#Username: VcJhVl8VY9
#Database name: VcJhVl8VY9
#Password: 2szV2WF4BO
#Server: remotemysql.com
#Port: 3306
#These are the username and password to log in to your database and phpMyAdmin

def connect():
    connection = pymysql.connect(
        host='remotemysql.com',
        user='VcJhVl8VY9',
        password='2szV2WF4BO',
        db='VcJhVl8VY9',
        charset='utf8mb4',
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
# 9. 25% к получаемому опыту с мис
