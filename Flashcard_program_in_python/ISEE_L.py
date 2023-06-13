import sys
import random
import shelve
import datetime
from datetime import timedelta, datetime, date
import pandas as pd
import numpy as np


def todays_list(words_a_day):
    df = pd.read_csv('isee_csv.csv')
    df = df.sample(df.shape[0])
    today = date.today()
    df_today = df.loc[pd.to_datetime(df['Date']) < pd.to_datetime(date.today())]
    df_today = df.iloc[:words_a_day,:]
    if df_today.shape[0] < words_a_day:
        new_words = words_a_day - df_today.shape[0]
        df_new = df[df['Date'].isnull()].iloc[:new_words,:]
        df_today = pd.concat([df_today, df_new], axis = 0)
    return df_today


def print_list():
    df_today = todays_list(20)
    print("\n\n\nLIST OF TODAY'S WORDS\n\n\n")
    row_item = "{:25}: {:60}"

    for index, row in df_today.iterrows():
        print(row_item.format(row[0], row[1]))
    main()


def to_cardlist(df_today):
    word_list_today = []
    for index, row in df_today.iterrows():
        wordcard = {}
        wordcard['index'] = index
        wordcard['word'] = row[0]
        wordcard['definition'] = row[1]
        wordcard['date'] = row[2]
        wordcard['consecutive right'] = row[3]
        wordcard['card used'] = 0
        word_list_today.append(wordcard)
    return word_list_today


def fc():
    df = pd.read_csv('isee_csv.csv')
    df_today = todays_list(10)
    word_list_today = to_cardlist(df_today)
    print("You have " + str(len(word_list_today)) + " words in today's list.\n\n\n")
    while len(word_list_today) > 0:
        print(word_list_today[0]['word'] + '\n\n')
        answer = input('Enter definition: ')
        print('\n\n' + word_list_today[0]['definition'] + '\n\n')
        card = word_list_today.pop(0)
        correct = input(
            ' Did you get the question right or wrong or have you mastered the concept (type r, w, m or q)? ')
        
        try:
            if correct[0].lower() == 'r':
                if card['card used'] == 0:
                    card['card used'] += 1
                    df.at[card['index'], 'Consecutive Right'] += 1
                    df.at[card['index'], 'Date'] = date.today(
                    ) + timedelta(days=card['consecutive right'] * 2)
                word_list_today.append(card)
            elif correct[0].lower() == 'm':
                if card['card used'] == 0:
                    card['card used'] += 1
                    df.at[card['index'], 'Consecutive Right'] += 1
                    df.at[card['index'], 'Date'] = date.today(
                    ) + timedelta(days=card['consecutive right'] * 2)
            elif correct[0].lower() == 'q':
                break
            else:
                if card['card used'] == 0:

                    card['card used'] += 1
                    df.at[card['index'], 'Consecutive Right'] = 1
                    df.at[card['index'], 'Date'] = date.today() + timedelta(days=1)
                word_list_today.append(card)
        except:
            df.to_csv('isee_csv.csv', index=False)
            print('An error has occoured.')
            print('Returning to main menu.')
            main()

        
    df.to_csv('isee_csv.csv', index=False)
    print('You have finished today\'s flashcards.')
    main()

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
    
