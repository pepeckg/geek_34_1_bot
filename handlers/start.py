import sqlite3
from aiogram import types, Dispatcher
from aiogram.utils.deep_linking import _create_link
from config import bot
from database.sql_commands import Database
from keyboards.inline_buttons import start_keyboard, admin_keyboard


async def start_button(message: types.Message):
    print(message)
    command = message.get_full_command()
    if command[1] != "":
        link = await _create_link(link_type="start", payload=command[1])
        owner = Database().sql_select_user_by_link_query(
            link=link
        )
        if owner[0]["telegram_id"] == message.from_user.id:
            await bot.send_message(
                chat_id=message.from_user.id,
                text="Ты не можешь использовать свою ссылку"
            )
            return
        print(f"owner: {owner}")
        try:
            Database().sql_insert_referral_query(
                owner=owner[0]['telegram_id'],
                referral=message.from_user.id
            )
        except sqlite3.IntegrityError:
            pass

    Database().sql_insert_user_query(
        telegram_id=message.from_user.id,
        username=message.from_user.username,
        first_name=message.from_user.first_name,
        last_name=message.from_user.last_name,
    )

    # await bot.send_message(
    #     chat_id=message.chat.id,
    #     text=f"Hello im your first bot",
    #     reply_markup=await start_keyboard()

    # )
    with open('C:/Users/User/pythonProject/geek_34_1_bot/media/bot_pic.jpg', 'rb') as photo:
        await bot.send_photo(
            chat_id=message.chat.id,
            photo=photo,
            caption=f"Hello {message.from_user.first_name} im your first bot",
            reply_markup=await start_keyboard()
        )

async def secret_word(message: types.Message):
    if message.from_user.id == 301020687:
        await bot.send_message(
            chat_id=message.from_user.id,
            text="Приветствую, хозяин!",
            reply_markup=await admin_keyboard()
        )
    else:
        await bot.send_message(
            chat_id=message.from_user.id,
            text="Вы не правы"

        )
async def admin_user_list_call(call: types.CallbackQuery):
    users = Database().sql_select_all_user_query()
    user_list = []
    for user in users:
        if user['username']:
            user_list.append(user['username'])
        else:
            user_list.append(user['first_name'])
    await bot.send_message(
        chat_id=call.from_user.id,
        text='\n'.join(user_list)
    )

def register_start_handlers(dp: Dispatcher):
    dp.register_message_handler(start_button, commands=['start'])
    dp.register_message_handler(secret_word, lambda word: "onezero" in word.text)
    dp.register_callback_query_handler(admin_user_list_call,
                                       lambda word: word.data == "admin_user_list")
