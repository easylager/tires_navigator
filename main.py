from aiogram import Bot, Dispatcher, executor, types
from config import token, user_id
from aiogram.dispatcher.filters import Text
from av_215 import main as av
from bamper_215 import main as bm
import asyncio
import random

bot = Bot(token, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot=bot)



@dp.message_handler(commands='start')
async def start(message: types.Message):
    start_buttons = ['Fresh tires', 'Models']
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_buttons)
    await message.answer("Let'start bussines" , reply_markup=keyboard)

@dp.message_handler(Text(equals='Fresh tires'))
async def fresh(message: types.Message):
    fresh_tires = av()
    print(len(fresh_tires))
    if len(fresh_tires) > 0:
        print('more then 0')
        for key, value in fresh_tires.items():
            tires = f'{value["Модель"]}\n' \
                    f'{value["Цена"]}\n' \
                    f'{value["Остаток протектора"]} - {value["Год"]}\n' \
                    f'{value["Cсылка"]}\n' \
                    f'{value["Телефон"]}\n' \
                    f'{value["Дата публикации"]}'
            await message.answer(tires)
    else:
        await message.answer("Пока нет свежих предложений")

async def news_every_minute():
    while True:
        fresh_tires = av()
        if len(fresh_tires) > 0:
            print('more then 0')
            for key, value in sorted(fresh_tires.items()):
                tires = f'{value["Модель"]}\n' \
                        f'{value["Цена"]}\n' \
                        f'{value["Остаток протектора"]} - {value["Год"]}\n' \
                        f'{value["Cсылка"]}\n' \
                        f'{value["Телефон"]}\n' \
                        f'{value["Дата публикации"]}\n' \
                        f'{value["Дата продвижения"]}'
                await bot.send_message(user_id, tires)
        fresh_bamper = bm()
        if len(fresh_bamper) > 0:
            print('more then 0')
            for key, value in sorted(fresh_bamper.items()):
                tires = f'{value["Модель"]}\n' \
                        f'{value["Цена"]}\n' \
                        f'{value["Остаток протектора"]} - {value["Год"]}\n' \
                        f'{value["Cсылка"]}\n' \
                        f'{value["Телефон"]}\n' \
                        f'{value["Описание"]}\n' \
                        f'{value["Дата публикации"]}'
                await bot.send_message(user_id, tires)
        await asyncio.sleep(random.randrange(60, 120))


def main():
    loop = asyncio.get_event_loop()
    loop.create_task(news_every_minute())
    executor.start_polling(dp)

if __name__ == '__main__':
    main()