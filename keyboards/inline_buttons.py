from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


async def start_keyboard():
    markup = InlineKeyboardMarkup()
    questionnaire_button = InlineKeyboardButton(
        "how are you mood",
        callback_data="start_questionnaire"
    )
    markup.add(questionnaire_button)
    return markup


async def questionnaire_one_keyboard():
    markup = InlineKeyboardMarkup()
    fine_button = InlineKeyboardButton(
        "Fine",
        callback_data="mood_fine"
    )
    bad_button = InlineKeyboardButton(
        "Bad",
        callback_data="mood_bad"
    )
    markup.add(fine_button)
    markup.add(bad_button)
    return markup