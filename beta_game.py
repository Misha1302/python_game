from random import *
from time import sleep
from helper import *

with open('in.txt.', encoding='utf-8') as f:
    words = f.read().split('\n')
main_T_or_F = True
points = 0

print('Здравствуйте, Вы начали игру.')
print('Если Вы хотит понять, как играть в эту игру введите "/инструкция".')
start = input('Иначе чтоб начать игру нажмите Enter: ')
while True:
    if start == '/инструкция':
        help()
        break
    elif start == '':
        break
    else:
        start = input('Вы можете ввести только "/инструкция" или нажать Enter: ')

sleep(0.4)
while main_T_or_F:
    print()
    print(f'Ваш результат: {points}. ')
    print('Сейчас начнётся новый раунд.')
    sleep(0.8)
    word = choice(words)
    printed_word = word
    T_or_F = False
    p1 = 0
    start_0_or_1 = 0
    vale = []
    input_let = []
    input_word = []
    tries = len(word) * 2
    letters = ['*'] * len(word)
    print()
    print(f'У Вас есть {tries} попыток.')
    while tries > 0 and '*' in letters and not T_or_F:
        if start_0_or_1 == 0:
            start_0_or_1 += 1
        else:
            print()
            print(f'У Вас осталось {tries} попыток')
            if len(input_let) != 0:
                input_let.sort()
                print('Введённые буквы: ', end=' ')
                print(*input_let, sep=', ', end='.\n')
            if len(input_word) != 0:
                input_word.sort()
                print('Введённые слова: ', end=' ')
                print(*input_word, sep=', ', end='.\n')
        print('Оставшиеся буквы: ', *letters, sep='')
        guess = input('Введите вашу букву: ')
        guess = guess.lower()
        print()
        if guess == '':
            print("Вы ничего не ввели, видимо Вы ошиблись, попробуйте ещё раз.")
        elif guess == '/подсказка':
            if p1 == 0:
                tries -= 1
                letters2 = letters[:]
                p1 += 1
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
                print('Вы уже использовали подсказку')
        elif guess == '/целиком':
            guess = input('Введите слово целиком: ')
            if len(guess) != len(word):
                print('Введённое Вами слово не может быть загаданным словом.')
                print('У них разное количество букв.')
            elif guess in input_word:
                print('Вы уже вводили это слово.')
            else:
                tries -= 1
                if guess == printed_word:
                    print('Вы угадали слово целиком!')
                    T_or_F = True
                else:
                    print('Вы не угадали слово целиком.')
                    input_word.append(guess)
            print()
        elif guess == '/инструкция':
            help()
        elif guess == '/рекорд':
            print(f'Ваш рекорд: {get_info('record.txt')}')
        elif guess == '/сброс':
            remove_file('record.txt', 0)
            print('Вы сбросли рекорд.')
            print('Теперь Ваш рекорд: 0.')
        elif len(guess) > 1:
            print('Вы ввели более одного символа сразу.')
            print('Либо Вы ошиблись, либо Вы неправильно ввели команду.')
            print('Возможные команды: "/подсказка", "/целиком", "/рекорд", "/сброс", "/инструкция".')
        elif guess == ' ':
            print("Вы ввели пробел, в этой игре все слова без пробелов.")
        elif ord(guess) < 1071 or ord(guess) > 1103:
            print('Вы ввели не русскую букву а все слова в этой игре состоят из только русских букв.')
        elif guess in input_let:
            print('Вы уже вводили эту букву, попробуйте другую.')
        elif guess in word:
            print('Вы угадали одну букву.')
            tries -= 1
            input_let.append(guess)
            while guess in word:
                ind = word.index(guess)
                letters[ind] = guess
                word = word[:ind] + '*' + word[ind + 1:]
        else:
            input_let.append(guess)
            tries -= 1
            print('Такой буквы нет!')
    else:
        if not T_or_F and '*' in letters and tries == 0:
            print('Вы потратили все попытки.')
            print(f'Загаданное слово: {printed_word}.')
            print('Вы проиграли.')
            print(f'Вы набрали {points} очков.')
            main_T_or_F = False
        else:
            words.remove(printed_word)
            if p1 == 0:
                points += 5
            points += tries
            print('Вы выиграли раунд!')
            if tries == 0:
                print('Вы потратили все попытки.')
            else:
                print(f'Вы истратили {len(word) * 2 - tries} из {len(word) * 2} попыток.')
            print(f'Загаданное слово: {printed_word}.')
if points > get_info('record.txt'):
    print('Поздравляем!\nВы поставили новый рекорд!')
    remove_file('record.txt', points)
