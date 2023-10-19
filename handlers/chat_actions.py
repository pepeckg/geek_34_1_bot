import sqlite3
import time
from aiogram import types, Dispatcher
from config import bot, GROUP_ID
from database.sql_commands import Database


async def chat_action(message: types.message):
    ban_words = ['fuck', 'bitch', 'damn']
    if message.chat.id in GROUP_ID:
        for word in ban_words:
            if word in message.text.lower().replace(" ", ""):
                user = Database().sql_select_ban_users(
                    telegram_id=message.from_user.id,
                )
                if user:
                    Database().sql_update_ban_user_query(
                        telegram_id=message.from_user.id,
                    )
                    if user[0]['count'] >= 3:
                        until_date = int(time.time()) + 300  # считать в секундах
                        await bot.restrict_chat_member(
                            chat_id=message.chat.id,
                            user_id=message.from_user.id,
                            permissions=types.ChatPermissions(
                                can_send_messages=False,  # Запретить отправку сообщений
                                can_send_media_messages=False,  # Запретить отправку медиа-сообщений
                                can_send_other_messages=False,  # Запретить отправку других типов сообщений
                                can_send_polls=False,  # Запретить отправку опросов
                            ),
                            until_date=until_date
                        )
                        await bot.send_message(chat_id=message.chat.id,
                                               text=f'Пользовватель {message.from_user.username} несерьезны человек.'
                                                    f' За это мы заблокировали его на {until_date} секунд.')
                else:
                    Database().sql_insert_ban_user_query(
                        telegram_id=message.from_user.id,
                        username=message.from_user.username)
                await bot.delete_message(
                    chat_id=message.chat.id,
                    message_id=message.message_id)

                await bot.send_message(
                    chat_id=message.chat.id,
                    text=f'Не ругайтесь в этом чате\n'
                         f'Username: {message.from_user.username}\n'
                         f'First-Name: {message.from_user.first_name}')


def register_chat_actions_handlers(dp: Dispatcher):
    dp.register_message_handler(chat_action)