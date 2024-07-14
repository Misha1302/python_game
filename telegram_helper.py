import sqlite3


def func_start_game(message_chat_id):
	connection = sqlite3.connect('my_database.db')
	cursor = connection.cursor()
	cursor.execute(f'''INSERT INTO Users VALUES({message_chat_id}, '0', '0')''')
	connection.commit()
	connection.close()


def get_info(message_chat_id):
	connection = sqlite3.connect('my_database.db')
	cursor = connection.cursor()
	cursor.execute(f'''SELECT current_game, record FROM Users WHERE user_id = {message_chat_id}''')
	result = cursor.fetchall()
	result = list(result[0])
	points, record = result
	connection.close()
	return points, record


def remove_info(message_chat_id, current_game_or_record, number):
	connection = sqlite3.connect('my_database.db')
	cursor = connection.cursor()
	cursor.execute(f'UPDATE Users SET {current_game_or_record} = {number} WHERE user_id = {message_chat_id} ')
	connection.commit()
	connection.close()


def check_word(func_word):
	for elem in func_word:
		if (ord(elem) < 1040 or ord(elem) > 1103) and elem != 'ё':
			return False
		else:
			return True
