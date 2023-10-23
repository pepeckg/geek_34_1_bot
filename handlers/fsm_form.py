import sqlite3
import random
import re

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from config import bot, DESTINATION
from database.sql_commands import Database



from keyboards.inline_buttons import (
    like_dislike_keyboard,
    edit_delete_form_keyboard,
    my_profile_register,
)
class FormStates(StatesGroup):
    nickname = State()
    bio = State()
    age = State()
    occupation = State()
    photo = State()


async def fsm_start_check(call: types.CallbackQuery):
    user_form = Database().sql_select_user_form_query(
        telegram_id=call.from_user.id
    )
    if user_form:
        await bot.send_message(
            chat_id=call.from_user.id,
            text='Вы уже зарегистрированы'
        )
    else:
        await bot.send_message(
            chat_id=call.from_user.id,
            text='Какой твой nickname')
        await FormStates.nickname.set()

async def fsm_start(call: types.CallbackQuery):
    await bot.send_message(
        chat_id=call.from_user.id,
        text='Какой твой nickname')
    await FormStates.nickname.set()

async def load_nickname(message: types.Message,
                        state: FSMContext):
    async with state.proxy() as data:
        data['nickname'] = message.text

    await bot.send_message(
        chat_id=message.from_user.id,
        text='Давай продолжим, расскажи о себе.')
    await FormStates.next()


async def load_bio(message: types.Message,
                   state: FSMContext):
    async with state.proxy() as data:
        data['bio'] = message.text
        print(data)

    await bot.send_message(
        chat_id=message.from_user.id,
        text='Укажи возраст\n'
             'используй только цифры\n'
             'Правильно: 25\n'
             'Неправильно: двадцать пять'
    )
    await FormStates.next()


async def load_age(message: types.Message,
                   state: FSMContext):
    try:
        if type(int(message.text)) != int:
            pass
        async with state.proxy() as data:
            data['age'] = message.text
            print(data)

        await bot.send_message(
            chat_id=message.from_user.id,
            text='Какая твоя профессия?'
        )
        await FormStates.next()
    except ValueError as e:
        await message.reply(
            text='Будь внимателен.\n'
                 'Попробуй еще раз'
        )
        await state.finish()
        return


async def load_occupation(message: types.Message,
                          state: FSMContext):
    async with state.proxy() as data:
        data['occupation'] = message.text
        print(data)

    await bot.send_message(
        chat_id=message.from_user.id,
        text='Осталось последнеее. ФОТО'
    )
    await FormStates.next()


async def load_photo(message: types.Message,
                     state: FSMContext):
    path = await message.photo[-1].download(
        destination_dir=DESTINATION
    )
    async with state.proxy() as data:
        user = Database().sql_select_user_form_query(
            telegram_id=message.from_user.id
        )
        if user:
            Database().sql_update_user_form_query(
                nickname=data['nickname'],
                bio=data['bio'],
                age=data['age'],
                occupation=data['occupation'],
                photo=path.name,
                telegram_id=message.from_user.id
            )
            with open(path.name, 'rb') as photo:
                await bot.send_photo(
                    chat_id=message.chat.id,
                    photo=photo,
                    caption=f"Nickname: {data['nickname']}\n"
                            f"Bio: {data['bio']}\n"
                            f"Age: {data['age']}\n"
                            f"Occupation: {data['occupation']}\n"
                )
            await bot.send_message(
                chat_id=message.from_user.id,
                text="Updated successfully"
            )
        else:
            Database().sql_insert_user_form_query(
                telegram_id=message.from_user.id,
                nickname=data['nickname'],
                bio=data['bio'],
                age=data['age'],
                occupation=data['occupation'],
                photo=path.name,
            )

            with open(path.name, 'rb') as photo:
                await bot.send_photo(
                    chat_id=message.chat.id,
                    photo=photo,
                    caption=f"Nickname: {data['nickname']}\n"
                            f"Bio: {data['bio']}\n"
                            f"Age: {data['age']}\n"
                            f"Occupation: {data['occupation']}\n"
                )
            await bot.send_message(
                chat_id=message.from_user.id,
                text='Регистрация закончена'
            )
        await state.finish()


async def my_profile_call(call: types.CallbackQuery):
    user_form = Database().sql_select_user_form_query(
        telegram_id=call.from_user.id
    )
    try:
        with open(user_form[0]["photo"], 'rb') as photo:
            await bot.send_photo(
                chat_id=call.from_user.id,
                photo=photo,
                caption=f"Nickname: {user_form[0]['nickname']}\n"
                        f"О себе: {user_form[0]['bio']}\n"
                        f"Возраст: {user_form[0]['age']}\n"
                        f"Профессия: {user_form[0]['occupation']}\n",
            reply_markup = await edit_delete_form_keyboard()
            )
    except IndexError:
        await bot.send_message(
            chat_id=call.from_user.id,
            text='Вы не прошли регистрацию',
            reply_markup=await my_profile_register()
        )
# async def random_profiles_call(call: types.CallbackQuery):
#     users = Database().sql_select_all_user_form_query()
#     random_form = random.choice(users)
#     with open(random_form['photo'], 'rb') as photo:
#         await bot.send_photo(
#             chat_id=call.from_user.id,
#             photo=photo,
#             caption=f"Nickname: {random_form['nickname']}\n"
#                     f"Bio: {random_form['bio']}\n"
#                     f"Age: {random_form['age']}\n"
#                     f"Occupation: {random_form['occupation']}\n",
#             reply_markup=await like_dislike_keyboard(
#                 owner_tg_id=random_form['telegram_id']
#             )
#         )
async def random_profiles_call(call):
    liker_telegram_id = call.from_user.id
    disliker_telegram_id = call.from_user.id
    users = Database().sql_select_all_user_form_query()
    liked_users = Database().get_liked_users(liker_telegram_id)
    disliked_users = Database().get_disliked_users(disliker_telegram_id)
    filtered_users = [user for user in users if user['telegram_id'] not in liked_users
                      and user['telegram_id'] not in disliked_users]

    if filtered_users:
        random_form = random.choice(filtered_users)
        with open(random_form['photo'], 'rb') as photo:
            await bot.send_photo(
                chat_id=call.from_user.id,
                photo=photo,
                caption=f"Nickname: {random_form['nickname']}\n"
                        f"Bio: {random_form['bio']}\n"
                        f"Age: {random_form['age']}\n"
                        f"Occupation: {random_form['occupation']}\n",
                reply_markup=await like_dislike_keyboard(
                    owner_tg_id=random_form['telegram_id']
                )
            )
    else:
        await bot.send_message(
            chat_id=call.from_user.id,
            text="Нет профелей которые вы не лайкнули"
        )



async def like_detect_call(call: types.CallbackQuery):
    # print(call.data)
    owner_tg_id = re.sub("user_form_like_", "", call.data)
    # print(owner_tg_id)
    try:
        Database().sql_insert_like_query(
            owner=owner_tg_id,
            liker=call.from_user.id
        )
    except sqlite3.IntegrityError:
        await bot.send_message(
            chat_id=call.from_user.id,
            text="You already liked form before"
        )
    except sqlite3.OperationalError:
        await bot.send_message(
            chat_id=call.from_user.id,
            text="You already liked form before"
        )
    finally:
        await random_profiles_call(call=call)

async def dislike_detect_call(call: types.CallbackQuery):
    # print(call.data)
    owner_tg_id = re.sub("user_form_dislike_", "", call.data)
    # print(owner_tg_id)
    try:
        Database().sql_insert_dislike_query(
            owner=owner_tg_id,
            disliker=call.from_user.id
        )
    except sqlite3.IntegrityError:
        await bot.send_message(
            chat_id=call.from_user.id,
            text="You already liked form before"
        )
    except sqlite3.OperationalError:
        await bot.send_message(
            chat_id=call.from_user.id,
            text="You already liked form before"
        )
    finally:
        await random_profiles_call(call=call)

async def delete_form_call(call: types.CallbackQuery):
    Database().sql_delete_form_query(
        owner=call.from_user.id
    )
    await bot.send_message(
        chat_id=call.from_user.id,
        text="Your Form Deleted successfully"
    )


def register_fsm_form_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(fsm_start_check,
                                       lambda call: call.data == "fsm_start_check")
    dp.register_callback_query_handler(fsm_start,
                                       lambda call: call.data == "fsm_start")
    dp.register_message_handler(load_nickname,
                                state=FormStates.nickname,
                                content_types=['text'])
    dp.register_message_handler(load_bio,
                                state=FormStates.bio,
                                content_types=['text'])
    dp.register_message_handler(load_age,
                                state=FormStates.age,
                                content_types=['text'])
    dp.register_message_handler(load_occupation,
                                state=FormStates.occupation,
                                content_types=['text'])
    dp.register_message_handler(load_photo,
                                state=FormStates.photo,
                                content_types=types.ContentTypes.PHOTO)
    dp.register_callback_query_handler(my_profile_call,
                                       lambda call: call.data == "my_profile")
    dp.register_callback_query_handler(random_profiles_call,
                                       lambda call: call.data == "random_profile")
    dp.register_callback_query_handler(like_detect_call,
                                       lambda call: "user_form_like_" in call.data)
    dp.register_callback_query_handler(dislike_detect_call,
                                       lambda call: "user_form_dislike_" in call.data)
    dp.register_callback_query_handler(delete_form_call,
                                       lambda call: call.data == "delete_profile")
