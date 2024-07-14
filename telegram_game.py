from random import choice

import telebot

from telegram_helper import *

tony_2_id = 6783437817
with open('in.txt', encoding='utf-8') as f:
	words = f.read().split('\n')
input_let = []
input_word = []
start_game = ''
word = ''
printed_word = ''
hint1 = 0
tries = 0
st1 = 0
record = 0
points = 0
fully = False
letters = []

try:
	bot = telebot.TeleBot('7258195722:AAHMIMi0Fwhj2mgRfUrAS6LCb20nKUAGUZQ')
except Exception as e:
	bot = None
	print(e)


@bot.message_handler(commands=['start'])
def handle_start(message):
	bot.send_message(message.chat.id, 'Здравстауйте, Вы запустили игрового бота.\n'
	                                  'Рекомендуем Вам ознакомиться с инструкцией отправив команду /help.')

	if message.chat.username is None:
		bot.send_message(tony_2_id, message.chat.first_name + ' ' + message.chat.last_name + ' запустил(а) бота.')
	else:
		bot.send_message(tony_2_id, '@' + (message.chat.username) + ' запустил(а) бота.')


@bot.message_handler(commands=['help'])
def handle_help(message):
	bot.send_message(message.chat.id, 'По команде /start_game запустится новый раунд.\n'
	                                  'Ваша задача угадать слово по буквам, за это можно получать очки.\n'
	                                  'Чем меньше Вы потратили попыток на угадывание слова, тем больше очков вы получите.\n'
	                                  'Когда Вы полностью угадаете слово или попытки закончатся,\n'
	                                  'текущий раунд завершится.Чтоб начать новый раунд снова отправьте команду.\n'
	                                  'По завершению раудна набранные Вами очки сохранятся,\n'
	                                  'НО ТОЛЬКО В ТОМ СЛУЧАЕ ЕСЛИ ВЫ НЕ ПРОИГРАЛИ!\n'
	                                  'Вы можете использовать подсказку отправив команду /hint, это откроет одну закрытую букву.\n'
	                                  'Однако использовать подсказку можно только ОДИН раз.\n'
	                                  'Если Вы угадали слово, не использовав подсказку, то получите дополнительно 5 очков.\n'
	                                  'Также Вы можете попробовать угадать слово целиком,\n'
	                                  'отправив команду /fully и потом само слово полностью.\n'
	                                  '(без использования этой команды нельзя будет вводить больше одного символа за раз)\n'
	                                  'Отправив команду /show_progress, будут отображены ваши очки и ваш рекорд.\n'
	                                  'Команда /reset_record сбросит Ваш рекорд.\n'
	                                  'Комада /help отобразит эту инструкцию к игре.\n'
	                                  'Во время запущенной игры необходимо соблюдать несколько правил:\n'
	                                  '1.Необходимо вводить только русские буквы.\n'
	                                  '2.Вводить можно только по одному символу.\n'
	                                  '2.1.Исключение команды: /hint, /fully, /help, /show_progress.\n'
	                                  '3.Вводить цифры нельзя.\n'
	                                  'Комадны /hint, /fully не работают, пока не запущена игра.\n'
	                                  'Команда /start, /reset_record не работает во время запущенной игры.\n'
	                                  'Начните новую игру прямо сейчас введя команду /start_game!')


@bot.message_handler(commands=['start_game'])
def handle_start_game(message):
	global start_game, word, printed_word, letters, input_let, tries, hint1, fully, input_word, st1
	global points, record
	if start_game == '':
		start_game = 'start'
		try:
			points, record = get_info(message.chat.id)
		except:
			if message.chat.username is None:
				bot.send_message(tony_2_id,
				                 'Зарегистирован новый пользователь под ником' + message.chat.first_name + ' ' + message.chat.last_name)
			else:
				bot.send_message(tony_2_id,
				                 'Зарегистирован новый пользоветель с usermane ' + '@' + (message.chat.username))
			func_start_game(message.chat.id)
			points, record = 0, 0
		st1 = 0
		hint1 = 0
		input_let = []
		input_word = []
		word = choice(words)
		printed_word = word
		tries = len(word) * 2
		letters = len(word) * ['*']
		fully = False
		# bot.send_message(message.chat.id, 'Cлово - ' + word)
		bot.send_message(message.chat.id, 'Вы начали новый раунд.\n'
		                                  f'Сейчас Ваш очки равны  {points}.\n'
		                                  f'У Вас есть {tries} попыток.')
	if tries > 0 and '*' in letters and not fully:
		c = ''
		if st1 == 0:
			st1 += 1
		else:
			c += f'У Вас осталось {tries} попыток.\n'
			if len(input_let) != 0:
				input_let.sort()
				c += f'Введённые буквы:  ' + ', '.join(str(s) for s in input_let) + '.\n'
			if len(input_word) != 0:
				input_word.sort()
				c += f'Введённые слова: {",".join(str(s) for s in input_word)} .\n'
		c += 'Оставшиеся буквы:  ' + ''.join(str(s) for s in letters) + '\n'
		c += 'Введите букву:'
		msg = bot.send_message(message.chat.id, c)
		bot.register_next_step_handler(msg, game)
	else:
		start_game = ''
		remove_info(message.chat.id, 'current_game', 0)
		if '*' in letters and tries == 0 and not fully:
			bot.send_message(message.chat.id, 'Вы истратили все попытки.\n'
			                                  'Вы не угадали слово.\n'
			                                  f'Задагаданное слово {printed_word}.\n'
			                                  'Вы проиграли.')
			bot.send_message(message.chat.id, f'Ваш результат: {points}.')
			if points > record:
				bot.send_message(message.chat.id, 'Поздравляем, Вы поставили новый рекорд!')
				remove_info(message.chat.id, 'record', points)
		else:
			points += tries
			if hint1 == 0:
				points += 5
			remove_info(message.chat.id, 'current_game', points)
			c = ''
			if not fully:
				c += 'Вы угадали слово.\n'
			else:
				c += 'Вы угадали слово целиком.\n'
			if tries == 0:
				c += 'Вы потратили все попытки.\n'
			else:
				c += f'Вы потратили {len(word) * 2 - tries} из {len(word) * 2} попыток.\n'
			c += f'Загаданное слово: {printed_word}.\n'
			c += 'Вы выиграли раунд.'
			bot.send_message(message.chat.id, c)
			bot.send_message(message.chat.id, f'Ваш результат: {points}.\n'
			                                  'Чтоб начать новый раунд отправте команду /start_game.')
		return


def game(message):
	global word, input_let, tries, start_game, letters, hint1
	not_main_fully = False
	if message.text is None:
		bot.send_message(message.chat.id, 'Ваш ввод нарушает правила!')
	else:
		guess = message.text.lower()
		if guess == '/help':
			handle_help(message)
		elif guess == '/fully':
			not_main_fully = True
			msg = bot.send_message(message.chat.id, 'Введите слово целиком:')
			bot.register_next_step_handler(msg, func_fully)
		elif guess == '/hint':
			if hint1 == 0:
				hint1 += 1
				tries -= 1
				letters2 = letters[:]
				vale = []
				while '*' in letters2:
					vale.append(letters2.index('*'))
					letters2[letters2.index('*')] = '!'
				can = choice(vale)
				letter = word[can]
				while letter in word:
					letters[word.index(letter)] = word[word.index(letter)].upper()
					word = word[:word.index(letter)] + '*' + word[word.index(letter) + 1:]
				input_let.append(letter)
			else:
				bot.send_message(message.chat.id, 'Вы уже использовали подсказку,\n'
				                                  'её можно использовать только один раз.')
		elif guess == '/show_progress':
			show_progress(message)
		elif len(guess) > 1 or (ord(guess) < 1040 or ord(guess) > 1103) and guess != 'ё':
			bot.send_message(message.chat.id, 'Ваш ввод нарушает правила игры.\n')
		elif guess in input_let:
			bot.send_message(message.chat.id, 'Вы уже вводили эту букву,\n'
			                                  'попробуйте другую.')
		elif guess in word:
			tries -= 1
			input_let.append(guess)
			bot.send_message(message.chat.id, 'Вы угадали, эта буква есть в слове.')
			while guess in word:
				ind = word.index(guess)
				letters[ind] = guess
				word = word[:ind] + '*' + word[ind + 1:]
		else:
			tries -= 1
			input_let.append(guess)
			bot.send_message(message.chat.id, 'Такой буквы нет.')
	if not not_main_fully:
		handle_start_game(message)


def func_fully(message):
	global tries, fully, input_word
	if message.text is None:
		bot.send_message(message.chat.id, 'Ваш ввод нарушает правила!')
	else:
		guess = message.text.lower()
		if not check_word(guess):
			bot.send_message(message.chat.id, 'В ведённом Вами слове есть сивол(ы),\n'
			                                  'которые нарушают правила игры.')
		elif len(guess) != len(printed_word):
			bot.send_message(message.chat.id, 'Введённое Вами слово не может быть загаданным словом.\n'
			                                  'У них разное количество букв.')
		elif guess in input_let:
			bot.send_message(message.chat.id, 'Вы уже вводили это слово,\n'
			                                  'попробуйте другое.')
		else:
			tries -= 1
			if guess == printed_word:
				fully = True
			else:
				input_word.append(guess)
				bot.send_message(message.chat.id, 'Вы не угадали слово целиком.')
	handle_start_game(message)


@bot.message_handler(commands=['show_progress'])
def show_progress(message):
	try:
		func_points, func_record = get_info(message.chat.id)
	except:
		func_points, func_record = 0, 0
	bot.send_message(message.chat.id, f'Ваши очки: {func_points}.\n'
	                                  f'Ваш рекорд: {func_record}.\n'
	                                  'Повысьте Ваш результат отправив команду /start_game.')


@bot.message_handler(commands=['reset_record'])
def reset_record(message):
	if start_game == '':
		try:
			remove_info(message.chat.id, 'record', 0)
		finally:
			bot.send_message(message.chat.id, 'Ваш рекорд сброшен.')


@bot.message_handler(
	content_types=['text', 'audio', 'document', 'photo', 'sticker', 'video', 'animation', 'video_note', 'voice',
	               'location', 'contact', 'pinned_message'])
def handle_message(message):
	if start_game == '':
		bot.send_message(message.chat.id, 'Начните новую игру, чтоб отправлять буквы и команды.\n'
		                                  'Чтоб начать новый раунд введите команду /start_game.')


bot.polling()
