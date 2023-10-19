from aiogram import types, Dispatcher
from config import bot
from keyboards.inline_buttons import questionnaire_one_keyboard


async def start_questionnaire(call: types.CallbackQuery):
    print(call)
    await bot.send_message(
        chat_id=call.message.chat.id,
        text="How are you?",
        reply_markup=await questionnaire_one_keyboard()
    )


async def fine_answer(call: types.CallbackQuery):
    print(call)
    await bot.send_message(
        chat_id=call.message.chat.id,
        text="I glad for you!",
    )


async def bad_answer(call: types.CallbackQuery):
    print(call)
    await bot.send_message(
        chat_id=call.message.chat.id,
        text="Drink same bear",
    )


def register_callback_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(start_questionnaire,
                                       lambda call: call.data == "start_questionnaire")
    dp.register_callback_query_handler(fine_answer,
                                       lambda call: call.data == "mood_fine")
    dp.register_callback_query_handler(bad_answer,
                                       lambda call: call.data == "mood_bad")
