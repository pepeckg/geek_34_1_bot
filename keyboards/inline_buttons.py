from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


async def start_keyboard():
    markup = InlineKeyboardMarkup()
    questionnaire_button = InlineKeyboardButton(
        "Ответь на вопрос.",
        callback_data="start_questionnaire"
    )
    registration_button = InlineKeyboardButton(
        "Регистрация",
        callback_data="fsm_start"
    )
    my_profile_button = InlineKeyboardButton(
        "Мой профиль",
        callback_data="my_profile"
    )
    markup.add(questionnaire_button)
    markup.add(registration_button)
    markup.add(my_profile_button)
    return markup


async def questionnaire_one_keyboard():
    markup = InlineKeyboardMarkup()
    fine_button = InlineKeyboardButton(
        "Хорошо",
        callback_data="mood_fine"
    )
    bad_button = InlineKeyboardButton(
        "Так себе",
        callback_data="mood_bad"
    )
    markup.add(fine_button)
    markup.add(bad_button)
    return markup


async def admin_keyboard():
    markup = InlineKeyboardMarkup()
    admin_user_list_button = InlineKeyboardButton(
        "Список смертных",
        callback_data="admin_user_list"
    )
    markup.add(admin_user_list_button)
    return markup
