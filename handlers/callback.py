import asyncio

from aiogram import types, Dispatcher
from config import bot
from keyboards.inline_buttons import questionnaire_one_keyboard
from scraping.news_scraper import NewsScraper
from scraping.async_scraper import AllNewsScraper

async def start_questionnaire(call: types.CallbackQuery):
    print(call)
    await bot.send_message(
        chat_id=call.message.chat.id,
        text="Ну как ты?",
        reply_markup=await questionnaire_one_keyboard()
    )


async def fine_answer(call: types.CallbackQuery):
    print(call)
    await bot.send_message(
        chat_id=call.message.chat.id,
        text="Я рад за тебя",
    )


async def bad_answer(call: types.CallbackQuery):
    print(call)
    await bot.send_message(
        chat_id=call.message.chat.id,
        text="Выпий пива",
    )

async def latest_news_call(call: types.CallbackQuery):
    scraper = NewsScraper()
    links = scraper.parse_data()
    for link in links:
        await bot.send_message(
            chat_id=call.message.chat.id,
            text=link,
        )


async def latest_news_by_group_call(call: types.CallbackQuery):
    scraper = AllNewsScraper()
    await scraper.scrape_all_groups()

    for group in scraper.list_news:
        links = await scraper.get_latest_links(group, limit=3) # больше ставлю начинает флудить и рубит
        if links:
            await bot.send_message(
                chat_id=call.message.chat.id,
                text=f"Последние 5 новостей в группе '{group}':",
            )
            for link in links:
                await bot.send_message(
                    chat_id=call.message.chat.id,
                    text=link,
                )
            await asyncio.sleep(10) # задержка между сообщениями которая помогает избежать флуд

def register_callback_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(start_questionnaire,
                                       lambda call: call.data == "start_questionnaire")
    dp.register_callback_query_handler(fine_answer,
                                       lambda call: call.data == "mood_fine")
    dp.register_callback_query_handler(bad_answer,
                                       lambda call: call.data == "mood_bad")
    dp.register_callback_query_handler(latest_news_call,
                                       lambda call: call.data == "latest_news")
    dp.register_callback_query_handler(latest_news_by_group_call,
                                       lambda call: call.data == "latest_news_by_group_call")