import environs
from telebot import TeleBot

import db
import messages as msg
import utils

env = environs.Env()
env.read_env(path='.env')

bot = TeleBot(env('BOT_TOKEN'), parse_mode='html')
ADMIN_ID = 6190447130


@bot.message_handler(commands=['start'])
def start(message):
    chat_id = message.chat.id
    first_name = message.from_user.first_name
    if db.get_user(chat_id) is not True:
        last_name = message.from_user.last_name
        username = message.from_user.username
        db.add_user(chat_id, first_name, last_name, username)
    bot.send_message(chat_id, msg.start(first_name))
    bot.send_message(chat_id, msg.SEND_MESSAGE)


@bot.message_handler(func=lambda message: message.chat.id != ADMIN_ID)
def forward_to_admin(message):
    bot.forward_message(ADMIN_ID, message.chat.id, message.message_id)


@bot.message_handler(func=lambda message: message.chat.id == ADMIN_ID and message.reply_to_message is not None)
def reply_to_user(message):
    forwarded_message = message.reply_to_message
    original_chat_id = forwarded_message.forward_from.id
    response_text = message.text
    try:
        bot.send_message(original_chat_id, response_text)
    except Exception as e:
        bot.send_message(ADMIN_ID, 'Error {}'.format(e))


@bot.message_handler(commands=['users'], func=lambda message: message.chat.id == ADMIN_ID)
def get_all_user(message):
    chat_id = message.chat.id
    info_users = db.get_full_info()
    bot.send_message(chat_id, utils.format_data(info_users))


if __name__ == '__main__':
    print('Starting...')
    bot.infinity_polling(skip_pending=True)
