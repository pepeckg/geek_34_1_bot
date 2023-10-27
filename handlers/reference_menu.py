from aiogram import types, Dispatcher
from aiogram.utils.deep_linking import _create_link
import binascii
import os
from config import bot
from database.sql_commands import Database
from keyboards.inline_buttons import (
    reference_menu_keyboard,
)


async def reference_menu_call(call: types.CallbackQuery):
    await bot.send_message(
        chat_id=call.from_user.id,
        text=f"Привет {call.from_user.first_name}\n"
             f"Реферальное меню готово",
        reply_markup=await reference_menu_keyboard()
    )


async def reference_link_call(call: types.CallbackQuery):
    user = Database().sql_select_user_query(
        telegram_id=call.from_user.id
    )
    print(user)

    if not user[0]['link']:
        token = binascii.hexlify(os.urandom(8)).decode()
        link = await _create_link(link_type="start", payload=token)
        print(link)
        Database().sql_update_user_reference_link_query(
            link=link,
            telegram_id=call.from_user.id
        )
        await bot.send_message(
            chat_id=call.from_user.id,
            text=f"Привет {call.from_user.first_name}\n"
                 f"Это твоя ссылка. Делись {link}",
        )
    else:
        await bot.send_message(
            chat_id=call.from_user.id,
            text=f"Привет {call.from_user.first_name}\n"
                 f"Это твоя созданная ссылка. Я взял ее из базы {user[0]['link']}",
        )


async def referral_list_call(call: types.CallbackQuery):
    referral_users = Database().sql_select_all_referral_by_owner_query(
        owner=call.from_user.id
    )
    data = []
    if referral_users:
        for user in referral_users:
            data.append(f"[{user['referral']}](tg://user?id={user['referral']})")
        text = '\n'.join(data)
        await bot.send_message(
            chat_id=call.from_user.id,
            text=text,
            parse_mode=types.ParseMode.MARKDOWN
        )


def register_reference_menu_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(reference_menu_call,
                                       lambda call: call.data == "reference_menu")
    dp.register_callback_query_handler(reference_link_call,
                                       lambda call: call.data == "reference_link")
    dp.register_callback_query_handler(referral_list_call,
                                       lambda call: call.data == "reference_list")