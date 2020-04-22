import vk_api
import random
from time import monotonic,sleep
from vk_api.longpoll import VkEventType, VkLongPoll
from adds import connect
import pymysql.cursors
from connection import register
import pymysql.cursors
import re
token = '9799c7774f89ef20c6503813c849b5d8e74c975c8d340e223f36ba47478108686da041b9214f8483b48cc'

vk = vk_api.VkApi(token=token)
vk._auth_token()
longpoll = VkLongPoll(vk)
actioncheck = 0
timestart = 0
timeend = 0
def send(message,keyboardt):
	vk.method("messages.send",{"peer_id":event.user_id,"random_id":0,"message":str(message),
							   "keyboard":open("keyboards/"+keyboardt+".json","r",encoding="UTF-8").read()})
def usend(message):
	vk.method("messages.send",{"peer_id":event.user_id,"random_id":0,"message":str(message)})

def sendto(message,user_id,keyboardt):
	vk.method("messages.send",{"peer_id":str(user_id),"random_id":0,"message":str(message),
							   "keyboard":open("keyboards/"+keyboardt+".json","r",encoding="UTF-8").read()})
def sendtou(message,user_id):
	vk.method("messages.send",{"peer_id":str(user_id),"random_id":0,"message":str(message)})
#MIssion начался
def mission():
	cursor.execute( f"SELECT timer FROM Users WHERE user_id = {event.user_id}" )
	qq = cursor.fetchone( )
	for i,a in qq.items( ):
		timer = a
	timestart=monotonic()
	cursor.execute(f"SELECT mtime FROM Users WHERE user_id={event.user_id}")  # Получаем время миссии
	qq=cursor.fetchone()
	timeend=0
	for i,a in qq.items():
		timeend=a

	if active==0:  # Одиночная миссия
		timer=random.choice(range(7,21))

		if timer<=10:
			send("[id" + str(event.user_id) + "|" + first_name + "], ты начал легкую миссию, это займет "+str(timer)+" минут.","missions")
			exps=1
			cursor.execute(f"UPDATE Users SET exps = 1, timer = {timer} WHERE user_id = {event.user_id}")
		if timer>=11 and timer<=15:
			send("[id" + str(event.user_id) + "|" + first_name + "], ты начал среднюю миссию, тебе придется попотеть, что бы выполнить ее тебе понадобится. "+str(timer)+" минут","missions")
			exps=2
			cursor.execute(f"UPDATE Users SET exps = 2, timer = {timer} WHERE user_id = {event.user_id}")
		if timer>=16:
			send("[id" + str(event.user_id) + "|" + first_name + "], ты начал сложную миссию. Она займет "+str(timer)+" минут. Удачи.","missions")
			exps=3
			cursor.execute(f"UPDATE Users SET exps = 3, timer = {timer} WHERE user_id = {event.user_id}")

		timeend=monotonic()+((timer-time2mis)*60)
		cursor.execute(f"UPDATE Users SET mtime = {timeend},active = 1 WHERE user_id = {event.user_id}")
		connection.commit()
	elif active >= 1 and timeend>timestart:  # Если миссия еще выполняется
		send("[id" + str(event.user_id) + "|" + first_name + "], вы уже заняты, закончите через "+str(int((timeend-timestart)/60))+" минут.","missions")
	elif timeend<timestart or (timer-monotonic()<=0):
		# Итог миссии
		if active == 1:
			cursor.execute( f"SELECT exps FROM Users WHERE user_id = {event.user_id}" )
			qq = cursor.fetchone( )
			for i,a in qq.items( ):
				exps = a
			cursor.execute( f"SELECT timer FROM Users WHERE user_id= {event.user_id}" )
			qq = cursor.fetchone( )
			for i,a in qq.items( ):
				timer = a
			exp = exps*timer*level*0.6*tenbonus*twentyfivebonus
			money = timer*exps*level*1.1*fivebonus*fivetybonus
			send( "[id" + str( event.user_id ) + "|" + first_name + "], ты закончил миссию и получил " + str(int( exp ) ) + " опыта вместе с горой монет(" + str( money ) + ")","missions" )
			cursor.execute(f"UPDATE Users SET active = 0,exp = exp + {int( exp )}, money = money + {int( money )} WHERE user_id = {event.user_id}" )
			connection.commit( )
		if active == 2:
			return raid()
		if active == 3:
			return grouprade()
	#Mission закончился
	#Рейд одиночный
def raid():
	cursor.execute( f"SELECT timer FROM Users WHERE user_id = {event.user_id}" )
	qq = cursor.fetchone( )
	for i,a in qq.items( ):
		timer = a
	timestart=monotonic()
	cursor.execute(f"SELECT mtime FROM Users WHERE user_id={event.user_id}")  # Получаем время миссии
	qq=cursor.fetchone()
	timeend=0
	for i,a in qq.items():
		timeend=a
	if active == 0:
		if level > 1:
			#Основной цикл
			timer=random.choice(range(16,31))

			if timer <= 22:
				send("[id" + str(event.user_id) + "|" + first_name + "], попалась маленькая база, а значит и добыча меньше. Думаю за "+str(timer)+" минут справишся.","missions")
				exps = 2
				cursor.execute(f"UPDATE Users SET exps = {exps}, timer = {timer} WHERE user_id = {event.user_id}")
			if 22 < timer <= 26:
				send("[id" + str(event.user_id) + "|" + first_name + "], мы нашли для тебя небольшую базу, что заберешь - все твое! На все это у тебя "+str(timer)+" минут. Удачи!","missions")
				exps = 3
				cursor.execute(f"UPDATE Users SET exps = {exps}, timer = {timer} WHERE user_id = {event.user_id}")
			if 28 < timer <= 30:
				send("[id" + str(event.user_id) + "|" + first_name + "], мы тут нашли базу и скажу тебе она не из самых легких. Огромная база с кучей оружия и людей внутри. Мы с командой даем тебе "+str(timer)+" минут. Что заберешь - все твое.","missions")
				exps = 4
				cursor.execute(f"UPDATE Users SET exps = {exps}, timer = {timer} WHERE user_id = {event.user_id}")

			timeend = monotonic()+((timer-time2mis)*60)
			cursor.execute(f"UPDATE Users SET mtime = {timeend}, active = 2 WHERE user_id = {event.user_id}")
			connection.commit()
	elif timeend<timestart:
		if active == 1:
			return mission()
		if active == 2:
			cursor.execute( f"SELECT exps FROM Users WHERE user_id = {event.user_id}" )
			qq = cursor.fetchone( )
			for i,a in qq.items( ):
				exps = a
			cursor.execute( f"SELECT timer FROM Users WHERE user_id= {event.user_id}" )
			qq = cursor.fetchone( )
			for i,a in qq.items( ):
				timer = a
			exp = exps*timer*1.1*tenbonus*twentyfivebonus
			money = timer*exps*0.6*fivebonus*fivetybonus
			bissines = exps*0.7*(timer-time2zav)
			send( "[id" + str( event.user_id ) + "|" + first_name + "], ты закончил рейд и получил " + str(
			int( exp ) ) + " опыта вместе с горой монет(" + str( int( money ) ) + "), захватили " + str(
			int( bissines ) ) + " заводов под ваше управление!","missions" )
			cursor.execute(
			f"UPDATE Users SET active = 0,exp = exp + {int( exp )}, money = money + {int( money )}, bissines = bissines + {int( bissines )}, btime = {int( ((timer*60) + monotonic( ))*1.1 )}, bbtime = {int( monotonic( ) )} WHERE user_id = {event.user_id}" )
			connection.commit()
		if active == 3:
			return grouprade()
	elif active >= 1 and timeend>timestart:
		send( "[id" + str( event.user_id ) + "|" + first_name + "], вы уже заняты, закончите через " + str(int( (timeend - timestart)/60 ) ) + " минут.","missions" )
	#Рейд окончен
	#Груповой рейд
def grouprade():
	cursor.execute( f"SELECT user_id FROM Users WHERE groupt = {group}" )
	qq = cursor.fetchall( )
	con = 0
	for a in qq:
		list.append( a )
		con += 1
	timestart = monotonic( )
	cursor.execute( f"SELECT mtime FROM Users WHERE user_id={event.user_id}" )  # Получаем время миссии
	qq = cursor.fetchone( )
	timeend = 0
	for i,a in qq.items( ):
		timeend = a
	cursor.execute(f"SELECT timer FROM Users WHERE user_id = {event.user_id}")
	qq = cursor.fetchone()
	for i,a in qq.items():
		timer = a
	cursor.execute ( f"SELECT user_id,level FROM Users WHERE groupt={group}" )
	qq = cursor.fetchall ( )
	con = 0
	con1 = 0
	list = [ ]
	list1 = [ ]
	for i in qq :
		list.append ( i )
		for a , m in i.items ( ) :
			con += 1
			list1.append ( m )
	if 1 in list1 :
		for i in list1 :
			if i == 1 :
				usend ( "[id" + str ( list1 [ i ] ) + "|Участник], не иммет 2 уровня!" )
				con1 = 1
	if con1 == 0:
		if con >= 2:
			if active == 0:
				if level > 1:
					if groupa == 1:
						#Основной цикл
						timer=random.choice(range(22,37))

						if timer <= 26:
							send("[id" + str(event.user_id) + "|" + first_name + "], вы нашли базу и залетаете на хату к соседям! Этот рейд займет "+str(timer)+" минут.","missions")
							exps = 3.5
							cursor.execute(f"UPDATE Users SET exps = {exps}, timer = {timer} WHERE user_id = {event.user_id}")
						if 26 < timer <= 30:
							send("[id" + str(event.user_id) + "|" + first_name + "], бабка с соседнего подьезда рассказала где есть база с огромным снаряжением. Вы потратите "+str(timer)+" минут своей драгоценной жизни!","missions")
							exps = 4.5
							cursor.execute(f"UPDATE Users SET exps = {exps}, timer = {timer} WHERE user_id = {event.user_id}")
						if 30 < timer <= 36:
							send("[id" + str(event.user_id) + "|" + first_name + "], оказывается в подвале есть скрытый склад оружия. Вы с бандой заваливаетесь туда и понимаете, что это займет "+str(timer)+" минут","missions")
							exps = 5.5
							cursor.execute(f"UPDATE Users SET exps = {exps}, timer = {timer} WHERE user_id = {event.user_id}")

						timeend = monotonic()+(timer*60)
						cursor.execute(f"UPDATE Users SET mtime = {timeend}, active = 3 WHERE user_id = {event.user_id}")
						connection.commit()
					else:
						send("Вы не глава группы что бы начинать эту миссию!","group5")

			elif active >= 1 and timeend>timestart:
				send( "[id" + str( event.user_id ) + "|" + first_name + "], вы уже заняты, закончите через " + str(int( (timeend - timestart)/60 ) ) + " минут.","missions" )
			elif timeend<timestart:
				if active == 1:
					return mission()
				if active == 2:
					return raid()
				if active == 3:
					cursor.execute(f"SELECT exps FROM Users WHERE user_id = {event.user_id}")
					qq = cursor.fetchone( )
					for i,a in qq.items( ):
						exps = a
					cursor.execute(f"SELECT timer FROM Users WHERE user_id= {event.user_id}")
					qq=cursor.fetchone()
					for i,a in qq.items():
						timer=a
					exp = exps*timer*1.8*twentyfivebonus*tenbonus
					money = timer*exps*1.5*fivebonus*fivetybonus
					bissines = exps*1.1*(timer-time2zav)
					send( "[id" + str( event.user_id ) + "|" + first_name + "], вы удачно отхватили " + str(int( exp ) ) + " опыта и " + str( int( money) ) + " PK, захватили "+str(int(bissines))+" бизнесс заводов!","missions" )
					cursor.execute(f"UPDATE Users SET active = 0,exp = exp + {int( exp )}, money = money + {int( money )}, bissines = bissines + {int(bissines)}, btime = {int(((timer*60)+monotonic())*1.1)}, bbtime = {int(monotonic())} WHERE user_id = {event.user_id}" )
					connection.commit()
		elif groupa == 1 and group > 0:
			send("[id" + str(event.user_id ) + "|" + first_name + "], нужно иметь минимум одного участника в отряде!","missions")
		elif groupa == 0 and group > 0:
			send("[id" + str(event.user_id ) + "|" + first_name + "], эту миссию может начать только глава отряда","missions")
		elif groupa == 0 and group == 0:
			send("[id" + str(event.user_id ) + "|" + first_name + "], вы не в отряде, что бы играть эту миссию","missions")



#Основной цикл
for event in longpoll.listen() :
	if event.type == VkEventType.MESSAGE_NEW and event.to_me :
		if event.from_chat or event.from_user :

			responseu = vk.method("users.get" , {"user_ids" : event.user_id})
			first_name = responseu[0]['first_name']
			response = event.text
			connection = connect()
			register(event.user_id)

			if response == "Начать" :
				with connection.cursor() as cursor :
					result = cursor.execute(f"SELECT user_id FROM Users WHERE user_id={event.user_id}")
					if result == 0 :
						register(event.user_id)
						send("[id" + str(
							event.user_id) + "|" + first_name + "], вы зарегистрировались в [public191654681|VKCyberpunk].\nДля получения большей информации о доступных командах напишите {Помощь}. \nНашли баги? Обращайтесь [mlgbet0808|сюда]." ,
							 "menu")
						connection.commit()
					else :
						send("[id" + str(event.user_id) + "|" + first_name + "], вы уже зарегистрированы." , "menu")

			with connection.cursor() as cursor :
				# Определняем начальные действия

				cursor.execute(f"SELECT money FROM Users WHERE user_id={event.user_id}")  # Получаю информацию о балансе
				qq = cursor.fetchone()
				if qq != None:
					for i , a in qq.items() :
						balance = a

				cursor.execute(f"SELECT bissines FROM Users WHERE user_id={event.user_id}")  # Получаю информацию о захваченых базах
				qq = cursor.fetchone()
				if qq != None:
					for i , a in qq.items() :
						bissines = a

				cursor.execute(f"SELECT level FROM Users WHERE user_id={event.user_id}")
				qq = cursor.fetchone()
				if qq != None:
					for i , a in qq.items() :
						level = a

				cursor.execute(f"SELECT user_id FROM Users")  # Получаю информацию о колличестве зарегистрированных
				qq = cursor.fetchall()
				playerscon = 0
				if qq != None:
					for i in qq :
						playerscon += 1

				cursor.execute(f"SELECT ban FROM Users WHERE user_id={event.user_id}") #Получаем статус игрока на наличие бана
				qq = cursor.fetchone()
				if qq != None:
					for i , a in qq.items() :
						ban = a

				cursor.execute(f"SELECT active FROM Users WHERE user_id={event.user_id}") #Узнаем, занимается ли наш игрок чем либо
				qq = cursor.fetchone()
				if qq != None:
					for i , a in qq.items() :
						active = a

				cursor.execute(f"SELECT exp FROM Users WHERE user_id = {event.user_id}") #Получаем информацию об опыте
				qq = cursor.fetchone()
				if qq != None:
					for i , a in qq.items():
						exp = a

				cursor.execute(f"SELECT groupt FROM Users WHERE user_id = {event.user_id}") #Получаем информацию об нахождении в отрядах
				qq = cursor.fetchone()
				if qq != None:
					for i, a in qq.items():
						group = a

				cursor.execute(f"SELECT groupa FROM Users WHERE user_id = {event.user_id}") #Получаем информацию об админе/участнике группы
				qq = cursor.fetchone()
				if qq != None:
					for i,a in qq.items():
						groupa = a

				cursor.execute(f"SELECT btime FROM Users WHERE user_id = {event.user_id}")
				qq = cursor.fetchone()
				if qq != None:
					for i, a in qq.items():
						btime = a

				# Определение Лвла
				cursor.execute(f"SELECT exp FROM Users WHERE user_id = {event.user_id}")
				qq = cursor.fetchone()
				if qq != None:
					for i, a in qq.items():
						exp = a

				cursor.execute(f"SELECT bbtime FROM Users WHERE user_id = {event.user_id}")
				qq = cursor.fetchone()
				if qq != None:
					for i , a in qq.items():
						bbtime = a

				cursor.execute(f"SELECT chance FROM Users WHERE user_id = {event.user_id}")
				qq = cursor.fetchone()
				if qq != None:
					for i , a in qq.items():
						chance = a

				cursor.execute(f"SELECT money FROM Users WHERE user_id = {event.user_id}")
				qq = cursor.fetchone()
				if qq != None:
					for i,a in qq.items():
						money = a

				cursor.execute(f"SELECT items FROM Users WHERE user_id = {event.user_id}")
				qq = cursor.fetchone()
				if qq != None:
					for i,a in qq.items():
						items = a

				cursor.execute(f"SELECT ref FROM Users WHERE user_id = {event.user_id}")
				qq = cursor.fetchone()
				if qq != None:
					for i,a in qq.items():
						ref = a

				#Заканчиваем опрделелять пользовательские данные
				fivebonus = 1
				tenbonus = 1
				time2mis = 0
				time2zav = 0
				cashback = 0
				otryad = 0
				fivetybonus = 1
				twentyfivebonus = 1
				if 10000000000 <= items < 19000000000:
					fivebonus = 1
				if 19000000000 < items < 19800000000:
					fivebonus = 1.05
				if 19800000000 < items < 19870000000:
					tenbonus = 1.10
				if 19870000000 < items < 19876000000:
					time2mis = 2
				if 19876000000 < items < 19876500000:
					time2zav = 2
				if 19876500000 < items < 19876540000:
					cashback = 5
				if 19876540000 < items < 19876543000:
					time2mis = 7
				if 19876543000 < items < 19876543200:
					otryad = 10
				if 19876543200 < items < 19876543210:
					fivetybonus = 1.15
				if 19876543210 < items < 19876543211:
					twentyfivebonus = 1.25
				if items == 19876543211:
					time2mis = 12
				# Бонусы ввиде предметов


				#Уровень
				if (125 < exp < 475) and (level == 1):
					cursor.execute(f"UPDATE Users SET level = 2 WHERE user_id = {event.user_id}")
					level = 2
					usend("Вы достигли 2 уровня!")
					connection.commit()
				if (475 < exp < 1360) and (level == 2):
					cursor.execute(f"UPDATE Users SET level = 3 WHERE user_id = {event.user_id}")
					level = 3
					usend("Вы достигли комед...&#129313; 3 уровня!")
					connection.commit()
				if (1360 < exp < 4960) and (level == 3):
					cursor.execute(f"UPDATE Users SET level = 4 WHERE user_id = {event.user_id}")
					level = 4
					usend("Что то долго я вас тут не видел, держи 4 уровень&#128126;")
					connection.commit()
				if (4960 < exp < 11090) and (level == 4):
					cursor.execute(f"UPDATE Users SET level = 5 WHERE user_id = {exent.user_id}")
					level = 5
					usend("Снова яЮ1213...1Ы&#128122;ФЫ Досто1Но УваЖЕния... ТУТ ПРОБЕЛмы со СВЯзьЮ... 5... 5 уровень... ")
					connection.commit()
				if (11090 < exp < 23670) and (level == 5):
					cursor.execute(f"UPDATE Users SET level = 6 WHERE user_id = {event.user_id}")
					level = 6
					usend(" у р о в е н ь 6")
					connection.commit()
				if (23670 < exp < 48140) and (level == 6):
					cursor.execute(f"UPDATE Users SET level = 7 WHERE user_id = {event.user_id}")
					level = 7
					usend("&#128128;7 уровень&#128128;")
					connection.commit()
				if (48140 < exp < 95600) and (level == 7):
					cursor.execute(f"UPDATE Users SET level = 8 WHERE user_id = {event.user_id}")
					level = 8
					usend("Ты наверное заждался! &#128575;Снова я и хочу сказать, что ты достиг 8 уровня! \n"
						  "УХУ. Ты реально задрот. Будешь у меня в таблицке висеть, пишу я кстати это в 2020, чтоб ты понимал, в общем. Поздравля..")
					connection.commit()
				if (95600 < exp < 200000) and (level == 8):
					cursor.execute(f"UPDATE Users SET level = 9 WHERE user_id = {event.user_id}")
					level = 9
					usend("&#128576;Как понимаешь 8 уровень был не предел! Это жесть... 9 лвл")
					connection.commit()
				if (200000 < exp) and (level == 9):
					cursor.execute(f"UPDATE Users SET level = 10 WHERE user_id = {event.user_id}")
					level = 10
					usend("&#128287; Молодец, теперь твое колличество опыта = твоим деньгам")
					expdas = 200000
					cursor.execute(f"UPDATE Users SET money = {expdas} WHERE user_id = {event.user_id}")
					connection.commit()
				# Заканчиваем определять начальные действия

				# Работаем с кнопками
				if ban == 0 :
					if "Профиль" in response:
						cursor.execute(f"SELECT exp FROM Users ")
						list = []
						con = 0
						while playerscon>0:
							qq = cursor.fetchone()
							for i,a in qq.items():
								list.append([a])
							playerscon -=1
							con += 1
						playerscon = con
						list.sort()
						for i in range(playerscon):
							if str(exp) in str(list[i]):
								top = playerscon - i



						send("[id" + str(event.user_id) + "|" + first_name + "], ваш профиль:\nВы на " + str(
							top) + " месте среди &#128285;" + str(playerscon) + "\nУ вас " + str(
							level) + " уровень ("+str(exp)+" опыта)""\nБаланс - " + str(balance) + " PK\nЗахвачено заводов - " + str(
							bissines) , "menu")

					if "Миссии" in response :
						send( "[id" + str (event.user_id ) + "|" + first_name + '], выберите тип миссии:\n'
																			 '   Секретная миссия\n'
																			 '   Одиночный рейд\n'
																			 '   Совместный рейд\n' , "missions" )

					if "Секретная миссия" in response:
						with connection.cursor ( ) as cursor :
							mission ( )

					if "Одиночный рейд" in response :
						with connection.cursor() as cursor:
							raid()

					if "Совместный рейд" in response:
						with connection.cursor() as cursor:
							grouprade()

					if "Назад" in response:
						send("[id" + str(event.user_id) + "|" + first_name + "], вы вернулись в меню." , "menu")
					#Склад
					if "Склад" in response:
						if items == 10000000001:
							send("Ваш склад пуст","storage")
						if items > 10000000001:
							text = "[id" + str(event.user_id) + "|" + first_name + "], ваши предметы:\n"
							if fivebonus == 1.05 and fivetybonus == 1:
								text = text + "Детектор - +5% получаемых монет\n"
							elif fivebonus == 1.05 and fivetybonus == 1.15:
								text = text + "Детектор вместе с сильным снаряжением - +20% получаемых монет\n"
							if fivebonus == 1 and fivetybonus == 1.15:
								text = text + "Сильное снаряжение - 15% получаемых монет\n"
							elif tenbonus == 1.10 and twentyfivebonus == 1:
								text = text + "Перчатки и маска - +10% получаемого опыта\n"
							elif tenbonus == 1 and twentyfivebonus == 1.25:
								text = text + "Экзоскелет - +25% получаемого опыта\n"
							elif tenbonus == 1.10 and twentyfivebonus == 1.25:
								text = text + "Перчатки с маской вместе с экзоскелетом - +37% получаемого опыта\n"
							if time2mis == 2:
								text = text + "Пониженый таймер - -2 минуты на выполнении миссии\n"
							elif time2mis == 7:
								text = text + "Пониженый таймер - -7 минут на выполнение миссии\n"
							elif time2mis == 12:
								text = text + "Пониженый таймер - -12 минут на выполнение миссии\n"
							if time2zav == 2:
								text = text + "Уменьшает время работы завода на 2 минуты\n"
							if cashback == 5:
								text = text + "Cash Back в казино с шансом 5%\n"
							if otryad == 10:
								text = text + "Размер отряда увеличен до 30 участников"
							send(text,"storage")




					if "Магазин" in response:
						usend("[id" + str(event.user_id) + "|" + first_name + "], 1. Детектор (200 PK) - увеличивает колличество получаемых монет с миссий на 5%\n"
							 " 2. Перчатки и маска (550 PK) - увеличивает колличество получаемого опыта с миссий на 10%\n"
							 " 3. Пониженый таймер (1250 PK) - время миссий сокращено на 2 минуты\n"
							 " 4. Активное производство (2780 PK) - уменьшает время работы заводов на 2 минуты\n"
							 " 5. Cash Back НА ВСЕ (4850 PK) - с 5% шансом возвращает проигранные средства в казино\n"
							 " 6. Пониженый таймер 2 (8940 PK) - время миссий сокращено на 7 минут\n"
							 " 7. Размер отряда увеличен до 30 человек (14750 PK)\n"
							 " 8. Сильное снаряжение (25000 PK) - увеличивает колличество получаемых монет с миссий на 15%\n"
							 " 9. Экзоскелет (38950 PK) - увеличивает колличество получаемого опыта с миссий на 25%\n"
							 " 10. Пониженый таймер 3 (50000 PK) - время миссий сокращено на 12 минут\n"
																			  "Что бы купить предмет используйте 'Купить ID_ПРЕДМЕТА'")
					if "Купить " in response:
						shop = 0
						shop = response.replace("Купить ","")
						result = re.findall( r'\D',str(shop))
						print(shop)
						print(result)
						if (result == []) and (1 <= int(shop) <= 10):
							if int(shop) == 1:
								if money > 200:
									if items < 19000000000:
										cursor.execute(f"UPDATE Users SET items = items + 9000000000, money = money - 200 WHERE user_id = {event.user_id}")
										connection.commit()
										usend("[id" + str(event.user_id) + "|" + first_name + "], вы успешно приобрели детектор! \nВаш баланс - "+str(money-200)+" PK")
									else:
										usend("У вас уже приобретен это предмет")
								else:
									usend("У вас не хватает денег для покупки! У вас "+str(money)+" PK, а нужно 200.")
							if int(shop) == 2:
								if money > 550:
									if items < 19800000000:
										cursor.execute(f"UPDATE Users SET items = items + 800000000, money = money - 550 WHERE user_id = {event.user_id}")
										connection.commit()
										usend("[id" + str(event.user_id) + "|" + first_name + "], вы успешно приобрели перчатки и маску! \nВаш баланс - "+str(money-550)+" PK")
									else :
										usend ( "У вас уже приобретен это предмет" )
								else :
									usend ( "У вас не хватает денег для покупки! У вас " + str (money ) + " PK, а нужно 550." )
							if int(shop) == 3:
								if money > 1250:
									if items < 19870000000:
										cursor.execute(f"UPDATE Users SET items = items + 70000000, money = money - 1250 WHERE user_id = {event.user_id}")
										connection.commit()
										usend("[id" + str(event.user_id) + "|" + first_name + "], вы успешно приобрели пониженый таймер! \nВаш баланс - "+str(money)+" PK")
									else :
										usend ( "У вас уже приобретен это предмет" )
								else :
									usend ( "У вас не хватает денег для покупки! У вас " + str (money ) + " PK, а нужно 1250." )
							if int(shop) == 4:
								if money > 2780:
									if items < 19876000000:
										cursor.execute(f"UPDATE Users SET items = items + 6000000, money = money - 2780 WHERE user_id = {event.user_id}")
										connection.commit()
										usend("[id" + str(event.user_id) + "|" + first_name + "], вы успешно приобрели активное производство! \nВаш баланс - "+str(money)+" PK")
									else :
										usend ( "У вас уже приобретен это предмет" )
								else :
									usend ( "У вас не хватает денег для покупки! У вас " + str (money ) + " PK, а нужно 2780." )
							if int(shop) == 5:
								if money > 4850:
									if items < 19876500000:
										cursor.execute(f"UPDATE Users SET items = items + 500000, money = money - 4850 WHERE user_id = {event.user_id}")
										connection.commit()
										usend("[id" + str(event.user_id) + "|" + first_name + "], вы успешно приобрели Cash Back! \nВаш баланс - "+str(money)+" PK")
									else :
										usend ( "У вас уже приобретен это предмет" )
								else :
									usend ( "У вас не хватает денег для покупки! У вас " + str (money ) + " PK, а нужно 4850." )
							if int(shop) == 6:
								if money > 8940:
									if items < 19876540000:
										cursor.execute(f"UPDATE Users SET items = items + 40000, money = money - 8940 WHERE user_id = {event.user_id}")
										connection.commit()
										usend("[id" + str(event.user_id) + "|" + first_name + "], вы успешно приобрели пониженый таймер 3! \nВаш баланс - "+str(money)+" PK")
									else :
										usend ( "У вас уже приобретен это предмет" )
								else :
									usend ( "У вас не хватает денег для покупки! У вас " + str ( money ) + " PK, а нужно 8940." )
							if int(shop) == 7:
								if money > 14750:
									if items < 19876543000:
										cursor.execute(f"UPDATE Users SET items = items + 3000, money = money - 14750 WHERE user_id = {event.user_id}")
										connection.commit()
										usend("[id" + str(event.user_id) + "|" + first_name + "], вы успешно увеличили размер отряда до 30 участников! \nВаш баланс - "+str(money)+" PK")
									else :
										usend ( "У вас уже приобретен это предмет" )
								else :
									usend ( "У вас не хватает денег для покупки! У вас " + str ( money ) + " PK, а нужно 14750." )
							if int(shop) == 8:
								if money > 25000:
									if items < 19876543200:
										cursor.execute(f"UPDATE Users SET items = items + 200, money = money - 25000 WHERE user_id = {event.user_id}")
										connection.commit()
										usend("[id" + str(event.user_id) + "|" + first_name + "], вы успешно приобрели сильное снаряжение! \nВаш баланс - "+str(money)+" PK")
									else :
										usend ( "У вас уже приобретен это предмет" )
								else :
									usend ( "У вас не хватает денег для покупки! У вас " + str ( money ) + " PK, а нужно 25000." )
							if int(shop) == 9:
								if money > 38950:
									if items < 19876543210:
										cursor.execute(f"UPDATE Users SET items = items + 10, money = money - 38950 WHERE user_id = {event.user_id}")
										connection.commit()
										usend("[id" + str(event.user_id) + "|" + first_name + "], вы успешно приобрели экзоскелет! \nВаш баланс - "+str(money)+" PK")
									else :
										usend ( "У вас уже приобретен это предмет" )
								else :
									usend ( "У вас не хватает денег для покупки! У вас " + str (
										money ) + " PK, а нужно 38950." )
							if int(shop) == 10:
								if money > 50000:
									if items < 19876543211:
										cursor.execute(f"UPDATE Users SET items = items + 1, money = money - 50000 WHERE user_id = {event.user_if}")
										connection.commit()
										usend("[id" + str(event.user_id) + "|" + first_name + "], вы успешно приобрели пониженый таймер 3! \nВаш баланс - "+str(money)+" PK")
									else :
										usend ( "У вас уже приобретен это предмет" )
								else :
									usend ( "У вас не хватает денег для покупки! У вас " + str (money ) + " PK, а нужно 50000." )

						else:
							usend("Неправильно введен ID_ПРЕДМЕТА\n"
								  "Используйте 'Купить ID_ПРЕДМЕТА', что бы купить предмет")

					#Реф. Системa
					if "Рефералка" in response:
						cursor.execute(f"SELECT user_id FROM Users WHERE ref = {event.user_id}")
						qq = cursor.fetchall( )
						list = [ ]
						ref = 0
						text = ""
						for a in qq:
							list.append( a )
							ref += 1
						list1 = [ ]
						for i in list:
							for a,m in i.items( ):
								list1.append( m )

						if ref == 0:
							send("[id" + str(event.user_id) + "|" + first_name + "], ваш реферальный код - "+str(event.user_id)+". Что бы стать вашим рефералом надо, что бы кто то другой написал 'Реферал "+str(event.user_id)+"'"++" \n"
																																										  " Ваши рефералы: их еще нету!","money")
						if ref >= 1:
							for i in range( ref ):
								text = text + "" + str( i + 1 ) + ". [id" + str( list1[ i ] ) + "|Реферал]\n"
								send( "[id" + str(event.user_id) + "|" + first_name + "], ваш реферальный код - " + str(
									event.user_id ) + ". Что бы стать вашим рефералом надо, что бы кто то другой написал 'Реферал " + str(
									event.user_id ) + "\n"
													  " Ваши рефералы: \n"+str(text)+"","money" )

					if "Реферал " in response:
						referal = 0
						referal = response.replace( "Реферал ","" )
						result = re.findall( r'\D',str( referal ) )
						if (result == [ ]) and (referal != 0):
							cursor.execute(f"SELECT user_id FROM Users WHERE user_id = {event.user_id}")
							qq = cursor.fetchall()
							con = 0
							for i in qq:
								con += 1
							if con == 1:
								if ref == 0:
									cursor.execute(f"UPDATE Users SET ref = {referal}money = money + 750 WHERE user_id = {event.user_id}")
									connection.commit()
									send("[id" + str(event.user_id) + "|" + first_name + "], вы стали рефералом и получили бесплатные 750 монет!","money")
									sendtou("[id" + str(event.user_id) + "|" + first_name + "], стал вашим рефералом",int(referal))
								else:
									usend("[id" + str(event.user_id) + "|" + first_name + "], вы уже стали чьим-то рефералом.")
							else:
								send("[id" + str(event.user_id) + "|" + first_name + "], такого реферального кода не существует","money")
						else:
							send("[id" + str(event.user_id) + "|" + first_name + "], обнаружены запрещенные символы, неправильно введен код!","money")
					#Финансы
					if "Финансы" in response:
						send("[id" + str(event.user_id) + "|" + first_name + "], что вы хотите сделать?","money")
					if "Собрать деньги с завода" in response:
						if btime > 0 and bissines > 0:
							if monotonic() > btime:
								pmoney = ((btime - bbtime)/60)*bissines*0.3
								cursor.execute(f"UPDATE Users SET btime = 0 WHERE user_id = {event.user_id}")
								send( "[id" + str(event.user_id ) + "|" + first_name + "], вы собрали " + str( pmoney ) + " PK","money" )
								cursor.execute(f"UPDATE Users SET money = money + {pmoney},bissines = 0,bbtime = 0,btime = 0 WHERE user_id = {event.user_id}" )
								connection.commit( )
							elif monotonic() < btime:
								pmoney = ((monotonic()-bbtime)/60)*bissines*0.3
								cursor.execute(f"UPDATE Users SET money = money + {pmoney}, bbtime = {monotonic()} WHERE user_id = {event.user_id}")
								send("[id" + str(event.user_id ) + "|" + first_name + "], вы собрали "+str(pmoney)+" PK","money")
								connection.commit()
						else:
							send("У вас нету захваченых заводов!","money")
					if "З-инфо" in response:
						send("[id" + str(event.user_id) + "|" + first_name + "], здесь начинается ваш бизнесс.\n"
																			 " Учавствуйте в рейдах и захватывайте заводы!\n"
																			 " Они же в свою очередь будут приносить временный доход.\n"
																			 " В любой момент вы можете пополнить VKCoin для прокачки! Курс 1000 VKCoin = 100 PK\n"
																			 " Для вывода же 100 PK = 950 VKCoin")
					#Казино
					if "Казино" in response:
						if level >= 2:
							send("[id" + str(
								event.user_id ) + "|" + first_name + "], что бы сделать ставку просто напиши: \n'Ставка КОЛИЧЕСТВО_МОНЕТ'. \nУ тебя шансы 50 на 50 для выигрыша.\n У тебя - "+str(money)+" монет","kazino")
						else:
							send("[id" + str(
								event.user_id ) + "|" + first_name + "], азартные игры разрешены с 2 лвла, у тебя "+str(level)+" уровень!","money")

					if "Ставка " in response:
						if level >= 2:
							if money >= 10:
								code = 0
								code = response.replace( "Ставка ","" )
								result = re.findall( r'\D',str( code ) )
								dlina = 0
								for i in code:
									dlina += 1
								if (result == [ ]) and (code != 0) and (0 < dlina < 9):
									stav = random.choice(range(100))
									if stav <= chance:
										send("[id" + str(event.user_id ) + "|" + first_name + "], ты  выйграл "+str(int(code)*2)+" монет. У тебя - "+str(money+int(code))+" монет!","kazino")
										cursor.execute(f"UPDATE Users SET money = money + {code} WHERE user_id = {event.user_id}")
										connection.commit()
									if stav > chance:
										send("[id" + str(event.user_id ) + "|" + first_name + "], ты проиграл "+str(int(code))+" монет. У тебя - "+str(money-int(code))+" монет!","kazino")
										cursor.execute(f"UPDATE Users SET money = money - {code} WHERE user_id = {event.user_id}")
										connection.commit()
								else:
									send("[id" + str(event.user_id ) + "|" + first_name + "], в значении ставка были запрещенные символы!","kazino")

							else:
								send("[id" + str(event.user_id ) + "|" + first_name + "], нужно иметь минимум 10 монет!","money")
						else:
							send( "[id" + str(
								event.user_id ) + "|" + first_name + "], азартные игры разрешены с 2 лвла, у тебя " + str( level ) + " уровень!","money" )

					#Помощь
					if "Помощь" in response:
						send("[id" + str(event.user_id) + "|" + first_name + "], все что вам нужно знать:\n"
																			 ' Профиль - важнейшая информация о вашем [public191654681|VKCyberpunk] аккаунте.\n' '\n'
																			 ' Миссии:\n'
																			 '   Секретная миссия - вы берете задание у курьера задание на выполнение которого дают деньги. После выполнения вам начислят PK и с редким шансом захваченый завод.\n'
																			 '   Одиночный рейд - вы в полном одиночестве нападаете на нейтральный завод и возможно захватываете его.\n'
																			 '   Cовместный рейд - вы собраным отрядом нападаете на нейтральный завод, c этого рейда вам начислят немного денег.\n' '\n'
																			 ' Отряд - могут присоединится только те кто знает ваш код отряда, вместе можно делать совместный рейд.\n' '\n'
																			 ' Склад - здесь хранятся ваши предметы.\n' '\n'
																			 ' Финансы - здесь вы можете отследить результат от захваченых заводов. Пополнить баланс и сыграть в казино.\n' ,
							 "menu")
					#ОТРЯД
					if "Отряд" in response:
						if group == 0:
							send( "[id" + str( event.user_id ) + "|" + first_name + "], вы не в отряде!",
								  "group1" )  # Вступить в группу | Создать отряд
						elif (group > 0) and (groupa == 0):
							send( "[id" + str( event.user_id ) + "|" + first_name + "], вы в отряде. " + str( group ),
								  "group5" )
						elif (group > 0) and (groupa == 1):
							send(
								"[id" + str( event.user_id ) + "|" + first_name + "], вы глава отряда. " + str( group ),
								"group4" )

					if "Вступить в отряд" in response:
						if group == 0:
							send( "[id" + str(
								event.user_id ) + "|" + first_name + "], что бы вступить в отряд напишите 'Присоединится КОД_ОТРЯДА'.",
								  "group1" )
						elif (group > 0) and (groupa == 0):
							send( "[id" + str( event.user_id ) + "|" + first_name + "], вы уже находитесь в отряде!",
								  "group5" )
						elif (group > 0) and (groupa == 1):
							send( "[id" + str(
								event.user_id ) + "|" + first_name + "], вы не можете вступить в новый отряд, т.к. в вы уже находитесь в отряде! Вы глава своего отряда!",
								  "group4" )

					if "Присоединится" in response:
						code = 0
						code = response.replace( "Присоединится ","" )
						result = re.findall( r'\D',str( code ) )
						dlina = 0
						for i in code:
							dlina += 1
						if (result == [ ]) and (code != 0) and (0 < dlina < 9):
							if group == 0:
								resulty = cursor.execute( f"SELECT groupt FROM Users WHERE groupt = {code}" )
								if 0 < resulty < 16:
									cursor.execute(
										f"UPDATE Users SET groupt = {code} WHERE user_id = {event.user_id}" )
									cursor.execute( f"SELECT user_id FROM Users WHERE groupa = 1 and groupt = {code}" )
									qq = cursor.fetchone( )
									for i,a in qq.items( ):
										user_id = a
									send( "[id" + str(
										event.user_id ) + "|" + first_name + "], вы присоеденились к отряду " + str(
										code ) + ".","group5" )
									sendto( "[id" + str(
										event.user_id ) + "|" + first_name + "] - присоединяется к вашему отряду!",
											str( user_id ) + ".","group4" )

							elif (group < 0) and (groupa == 1):
								send( "[id" + str(
									event.user_id ) + "|" + first_name + "], вы уже являетесь главой отряда!","group4" )
							else:
								send( "[id" + str( event.user_id ) + "|" + first_name + "], вы уже в отряде!","group5" )
						else:
							send( "[id" + str(
								event.user_id ) + "|" + first_name + "], вы ввели неверные символы или введеный код превышает 8 значений!",
								  "group3" )

					if "Создать отряд" in response:
						if group == 0:
							send( "[id" + str(
								event.user_id ) + "|" + first_name + "], выбери, как создаем твой секретный код?",
								  "group3" )
						elif (group > 0) and (groupa == 0):
							send( "[id" + str( event.user_id ) + "|" + first_name + "], вы уже находитесь в отряде!",
								  "group5" )
						elif (groupa == 1) and (group > 0):
							send( "[id" + str( event.user_id ) + "|" + first_name + "], вы уже глава в отряде!",
								  "group4" )

					if "Создать свой" in response:
						if group == 0:
							send( "[id" + str(
								event.user_id ) + "|" + first_name + "], напиши:\n 'Создать код {код}'\n Важно! Код должен содержать только цифры и только меньше 8!",
								  "group3" )
						if (group > 0) and (groupa == 0):
							send( "[id" + str( event.user_id ) + "|" + first_name + "], вы уже находитесь в отряде!",
								  "group5" )
						if (group > 0) and (groupa == 1):
							send( "[id" + str( event.user_id ) + "|" + first_name + "], вы уже управляете отрядом!",
								  "group4" )

					if "Выгнать" in response:
						if (groupa == 1) and (group > 0):
							word = response.replace( "Выгнать ","" )
							result = re.findall( r'\D',str( word ) )
							dlina = 0
							for i in word:
								dlina += 1
							if (result == [ ]) and (word != 0) and (0 < dlina < 10):
								cursor.execute( f"SELECT user_id FROM Users WHERE user_id={word}" )
								qq = cursor.fetchone( )
								if active == 0:
									if qq != [ ]:
										cursor.execute( f"SELECT user_id FROM Users WHERE user_id = {word}" )
										qq = cursor.fetchone( )
										for i,a in qq.items( ):
											user_id = a
										sendto( "Вы были выгнаны из отряда игроком - [id" + str(
											event.user_id ) + "|" + first_name + "]!",user_id,"group1" )
										cursor.execute( f"UPDATE Users SET groupt = 0 WHERE user_id = {word}" )
										connection.commit( )
									else:
										send( "Такого пользователя не существует","group4" )
								else:
									usend("Вы не можете выгнать участника не завершив миссию")
							else:
								send( "Неверно введен ID пользователя!","group4" )

					if "Создать код" in response:
						code = 0
						code = response.replace( "Создать код ","" )
						result = re.findall( r'\D',str( code ) )
						dlina = 0
						for i in code:
							dlina += 1
						if (result == [ ]) and (code != 0) and (0 < dlina < 9):
							if group == 0:
								resulty = cursor.execute( f"SELECT groupt FROM Users WHERE groupt = {code}" )
								if resulty == 0:
									cursor.execute(
										f"UPDATE Users SET groupt = {code},	groupa = 1 WHERE user_id = {event.user_id}" )
									connection.commit( )
									send( "[id" + str(
										event.user_id ) + "|" + first_name + "], вы создали свой отряд. \nЧто бы кто-то присоеденился к вашему отряду пусть он напишет 'Присоединится " + str(
										code ) + "'.","group4" )
								else:
									send( "[id" + str(
										event.user_id ) + "|" + first_name + "], отряд с таким кодом уже существует! Выберите другой!",
										  "group3" )
							else:
								send( "[id" + str( event.user_id ) + "|" + first_name + "], вы уже в отряде!","group4" )
						else:
							send( "[id" + str(
								event.user_id ) + "|" + first_name + "], вы ввели неверные символы или ваш код превышает 8 значений!",
								  "group3" )

					if "Создать рандомно" in response:
						if group == 0:
							group = random.randint( 0,99999999 )
							cursor.execute(
								f"UPDATE Users SET groupt = {group},groupa = 1 WHERE user_id = {event.user_id}" )
							connection.commit( )
							send( "[id" + str(
								event.user_id ) + "|" + first_name + "], вы создали свой отряд! \nЧто бы кто-то присоеденился к вашему отряду пусть он напишет 'Присоеденится " + str(
								group ) + "'.","group4" )
						elif (groupa == 0) and (group > 0):
							send( "[id" + str( event.user_id ) + "|" + first_name + "], вы уже в отряде!","group5" )
						elif (groupa == 1) and (group > 0):
							send( "[id" + str( event.user_id ) + "|" + first_name + "], вы уже управляете отрядом!",
								  "group4" )

					if "Вернуться в отряд" in response:
						if (groupa == 0) and (group == 0):
							send( "[id" + str( event.user_id ) + "|" + first_name + "], вы вернулись в меню отряда.",
								  "group1" )
						elif (groupa == 0) and (group > 0):
							send( "[id" + str( event.user_id ) + "|" + first_name + "], вы вернулись в отряд.",
								  "group5" )
						elif (groupa == 1) and (group > 0):
							send( "[id" + str( event.user_id ) + "|" + first_name + "], вы вернулись в отряд.",
								  "group4" )

					if "Распустить отряд" in response:
						if active == 0:
							if (groupa == 1) and (group > 1):
								result = cursor.execute(
									f"SELECT user_id FROM Users WHERE groupt = {group} and groupa = 0" )
								print( result )
								list = [ ]
								for i in range( result ):
									qq = cursor.fetchone( )
									for i,a in qq.items( ):
										list.append( a )
								print( list )
								for i in range( result ):
									sendto( "[id" + str( event.user_id ) + "|Глава], распустил отряд!",list[ i ],"group1" )
								cursor.execute( f"UPDATE Users SET groupt = 0, groupa = 0 WHERE groupt = {group}" )
								connection.commit( )
								send( "[id" + str( event.user_id ) + "|" + first_name + "], вы распустили отряд.","group1" )
							elif (groupa == 0) and (group > 0):
								send( "[id" + str( event.user_id ) + "|" + first_name + "], вы не являетесь главой отряда!",
									  "group5" )
							elif (groupa == 0) and (group == 0):
								send( "[id" + str( event.user_id ) + "|" + first_name + "], вы и так не в отряде!",
									  "group1" )
						else:
							usend("[id" + str( event.user_id ) + "|" + first_name + "], вы не можете распустить отряд во время миссии!")

					if "Покинуть отряд" in response:
						if active == 0:
							if (groupa == 0) and (group > 0):
								cursor.execute( f"SELECT user_id FROM Users WHERE groupa = 1 and groupt = {group}" )
								qq = cursor.fetchone( )
								for i,a in qq.items( ):
									user_id = a
								sendto( "[id" + str( event.user_id ) + "|" + first_name + "], покинул ваш отряд " + str(
									group ) + ".",str( user_id ),"group4" )
								cursor.execute( f"UPDATE Users SET groupt = 0 WHERE user_id = {event.user_id}" )
								send( "[id" + str( event.user_id ) + "|" + first_name + "], вы покинули отряд","group1" )
								connection.commit( )
							elif (groupa == 1) and (group > 0):
								send( "[id" + str(
									event.user_id ) + "|" + first_name + "], вы не можете покинуть свой отряд!\n Выберите кнопку 'Распустить отряд' т.к. вы глава отряда!",
								  	"group4" )
							elif (group == 0) and (groupa == 0):
								send( "[id" + str( event.user_id ) + "|" + first_name + "], вы и так не в отряде!",
								 	 "group1" )
						else:
							usend("Вы не можете покинуть отряд во время миссии!")

					if "Удалить с отряда" in response:
						if (groupa == 1) and (group > 0):
							send( "Напишите кого вы хотиты выгнать - 'Выгнать ID_ПОЛЬЗОВАТЕЛЯ'.","group4" )
						elif (groupa == 0) and (group > 0):
							send( "Вы не глава группы, что бы кого-то выгонять!","group5" )
						elif (group == 0) and (group == 0):
							send( "Вы не в отряде, что бы кого то выгонять!" )

					if "Состав отряда" in response:
						cursor.execute( f"SELECT user_id FROM Users WHERE groupt = {group}" )
						qq = cursor.fetchall( )
						list = [ ]
						con = 0
						for a in qq:
							list.append( a )
							con += 1
						text = "[id" + str( event.user_id ) + "|" + first_name + "], состав " + str( group ) + ":\n"
						list1 = [ ]
						for i in list:
							for a,m in i.items( ):
								list1.append( m )
						for i in range( con ):
							text = text + "" + str( i + 1 ) + ". [id" + str( list1[ i ] ) + "|Участник]\n"
						if (groupa == 0) and (group > 0):
							send( text,"group5" )

						if (groupa == 1) and (group > 0):
							send( text,"group4" )

						if (groupa == 0) and (group == 0):
							send( "Вы не в группе!","group1" )

					if "О-инфо" in response:
						if group == 0:
							send( "[id" + str( event.user_id ) + "|" + first_name + "], Отряд создать очень легко: \n"
																					"		Вступить в отряд - как сразу вы  нажмете на эту кнопку вам нужно будет ввести секретный код группы к которой вы хотите присоеденится.\n"
																					"		Создать отряд - бот генерирует секретный код группы, дальше отправляете этот код своим друзьями и начинайте играть.\n"
																					"		Распустить отряд - только создатель отряда может его распустить, или участники могут его покинуть. ",
								  "group1" )
						if (group > 0) and (groupa == 0):
							send( "[id" + str(
								event.user_id ) + "|" + first_name + "], вы вступили в отряд и не знаете что делать?\n"
																	 " Сейчас мы это подправим!\n"
																	 " Вступив в отряд вы можете учавствовать в совметных рейдах! "
																	 "Чем больше у вас уровни тем больше будет награда. \n"
																	 "Если тебе надоест сидеть в отряде то ты всегдя можешь его покинуть нажав на 'Покинуть отряд.'",
								  "group5" )
						if (group > 0) and (groupa == 1):
							send( "[id" + str(
								event.user_id ) + "|" + first_name + "], вы создали отряд и незнаете что дальше делать?\n"
																	 " Ну это мы мигом.\n"
																	 " Создав отряд скорее приглашайте друзей в свой отряд, что бы друг присоединился к вашей группе ему нужно написать 'Присоединится КОД_ВАШЕЙ_ГРУППЫ'.\n"
																	 " Код можно узнать написав 'Отряд' или 'Состав отряда'.\n"
																	 " Вместе вы сможете делать совметные рейды! И получать много опыта, ведь это зависит от уровней людей в отряде!",
								  "group4" )
