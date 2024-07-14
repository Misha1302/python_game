from random import *
p1 = 0
vale = []
word = 'телевидение'
input_let = []
tries = len(word) * 2
letters = ['*'] * len(word)

guess = '/подсказка'
if guess == '/подсказка' and p1 == 0:
    letters2 = letters[:]
    p1 += 1
    for i in range(letters2.count('*')):
        vale.append(letters2.index('*'))
        letters2[letters2.index('*')] = '!'
    can = choice(vale)
    letter = word[can]
    for i2 in range(word.count(letter)):
        letters[word.index(letter)] = word[word.index(letter)].upper()
        word = word[:word.index(letter)] + '*' + word[word.index(letter) + 1:]
    input_let.append(letter)
