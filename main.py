#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This program is dedicated to the public domain under the CC0 license.

"""
Basic example for a bot that uses inline keyboards.
"""
import sudoku_gen
import logging
import telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
import solver

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)


def start(update, context):
    keyboard = [
        [
            telegram.KeyboardButton("Сгенерировать судоку"),
            telegram.KeyboardButton("Решить судоку"),
        ]
    ]

    reply_markup = telegram.ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)

    update.message.reply_text("Добро пожаловать в бота, цель которого заключается в генерации/решении судоку. Пожалуйста выберите то, за чем вы здесь", reply_markup=reply_markup)


def button(update, context):
    msg = update.message.text
    keyboard = [
        [
            telegram.KeyboardButton("Сгенерировать судоку"),
            telegram.KeyboardButton("Решить судоку"),
        ]
    ]

    reply_markup = telegram.ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)

    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    if msg == "Сгенерировать судоку":
        game  = sudoku_gen.sudoku(3).field
        s = ''
        for j in range(len(game)):
            _ = game[j]
            if j % 3 == 0:
                s+= '-'*33+'\n'
            for i in range(9):
                if i %3 != 0:
                    s+=str(_[i])+' '
                else:
                    s+='| ' + str(_[i])+' '
            s+='|\n'
        s+= '-'*33+'\n'
        keyboard = [
            [telegram.InlineKeyboardButton("Ответ", callback_data='1')]
        ]
        reply_markup = telegram.InlineKeyboardMarkup(keyboard)
        update.message.reply_text(s, reply_markup=reply_markup)
    elif msg == 'Решить судоку':
        update.message.reply_text(text = 'Отправляйте головоломку строка за строкой.На месте пропусков ставьте 0.Не ставьте пробелы между цифрами. Вся головоломка должна быть в одном сообщении.')
    elif len(msg) == 89:
        try:
            msg = msg.split('\n')
            for i in range(9):
                int(msg[i])
            try:
                game = [[0 for i in range(9)] for j in range(9)] 
                for i in range(9):
                    for j in range(9):
                        game[i][j] = int(msg[i][j])
                s=''
                for solution in solver.solve_sudoku((3, 3), game):
                    for j in range(len(game)):
                        _ = game[j]
                        if j % 3 == 0:
                            s+= '-'*33+'\n'
                        for i in range(9):
                            if i %3 != 0:
                                s+=str(_[i])+' '
                            else:
                                s+='| ' + str(_[i])+' '
                        s+='|\n'
                    s+= '-'*33+'\n'
                    update.message.reply_text(text ='Решение: \n'+s, reply_markup = reply_markup)
            except:
                update.message.reply_text(text ='Судоку не имеет решения', reply_markup = reply_markup)
        except:
            update.message.reply_text(text ='Вы допустили ошибку в вводе', reply_markup = reply_markup)


def buttons(update, context):
    msg = update._effective_message.text
    query = update.callback_query

    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    query.answer()
    if query.data == '1':
        game = [[0 for i in range(9)] for j in range(9)]
        msg = msg.split('\n')
        for i in range(len(msg)):
            msg[i] = msg[i].split(' ')
        q = 0
        w = 0
        for i in msg:
            for j in i:
                try:
                    game[q][w] = int(j)
                    w+= (q+1)//9
                    q = (q+1)%9
                except:
                    ...
        s = ''
        for solution in solver.solve_sudoku((3, 3), game):
            for j in range(len(game)):
                _ = game[j]
                if j % 3 == 0:
                    s+= '-'*33+'\n'
                for i in range(9):
                    if i %3 != 0:
                        s+=str(_[i])+' '
                    else:
                        s+='| ' + str(_[i])+' '
                s+='|\n'
            s+= '-'*33+'\n'
        query.edit_message_text(s + "\nРешите, что делать дальше")
    
def help_command(update, context):
    update.message.reply_text("Use /start to test this bot.")


def main():
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater("775451016:AAHaigX22GeUIpkwtH2w8SNHG1slKhDYibc", use_context=True)

    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CommandHandler('help', help_command))
    updater.dispatcher.add_handler(CallbackQueryHandler(buttons))
    updater.dispatcher.add_handler(telegram.ext.MessageHandler(filters = telegram.ext.filters.Filters.text ,callback = button))

    # Start the Bot
    updater.start_polling()

    # Run the bot until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT
    updater.idle()


if __name__ == '__main__':
    main()