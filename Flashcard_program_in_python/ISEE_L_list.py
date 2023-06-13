


import sys
import random
import shelve
import datetime
from datetime import timedelta, datetime, date
import pandas as pd
import numpy as np


def to_cardlist(df):
    word_list = []
    for index, row in df.iterrows():
        wordcard = {}
        wordcard['index'] = index
        wordcard['word'] = row[0]
        wordcard['definition'] = row[1]
        wordcard['consecutive right'] = row[3]
        word_list.append(wordcard)
    return word_list


def card_return(answer, card):
    if answer[0].lower() == 'r':
        try:
            word_list = word_list[:card['consecutive right']*5] + \
                card + word_list[card['consecutive right']*5:]
        except:
            print('Error in card_return')
            word_list.append(card)
    elif answer[0].lower() == 'm':
        try:
            word_list = word_list[:card['consecutive right']*10] + \
                card + word_list[card['consecutive right']*10:]
        except:
            print('Error in card_return')
            word_list.append(card)
    else:
        try:
            word_list = word_list[:5] + card + word_list[5:]
        except:
            print('Error in card_return')
            word_list.append(card)


def print_list():
    df_today = to_list(20)
    print("\n\n\nLIST OF TODAY'S WORDS\n\n\n")
    row_item = "{:25}: {:60}"

    for index, row in df_today.iterrows():
        print(row_item.format(row[0], row[1]))
    main()





def fc():
    df = pd.read_csv('isee_csv.csv')

    word_list = to_cardlist(df)

    for card in word_list[:10]:
        print(card)

    print("You have " + str(len(word_list)) + " words in today's list.\n\n\n")
    while len(word_list) > 0:
        print(word_list[0]['word'] + '\n\n')
        answer = input('Enter definition: ')
        print('\n\n' + word_list[0]['definition'] + '\n\n')
        card = word_list.pop(0)
        correct = input(
            ' Did you get the question right or wrong or have you mastered the concept (type r, w, m or q)? ')
        try:
            if correct[0].lower() == 'r':
                card['consecutive right'] += 1
                card_return('r', card)
            elif correct[0].lower() == 'm':
                card['consecutive right'] += 1
                card_return('m', card)
            elif correct[0].lower() == 'q':
                break
            else:
                card['consecutive right'] = 1
                card_return('w', card)
        except:
            df.to_csv('isee_csv_list.csv', index=False)
            print('An error has occoured.')
            print('Returning to main menu.')

        
    df.to_csv('isee_csv_list.csv', index=False)

def main():
    print("\n\n\nFlashcards: Main Menu\n\n")
    print("Print list of today's flashcards: Press['1']\n")
    print("Run today's flashcards:           Press['2']\n")
    print("Quit:                             Press['3']\n")
    menu_choice = input("> ")
    if menu_choice == '1':
        print_list()
    elif menu_choice == '2':
        fc()
    elif menu_choice == '3':
        sys.exit
    else:
        print("Invalid Entry\n\n\n")
        main()

  


main()
    
