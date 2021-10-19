from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
from aiogram.utils.markdown import hbold, hlink
from config import TOKEN, CACHE_PATH, TARGET_ELO
from main import get_stats
import json

bot = Bot(token=TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)

@dp.message_handler(commands='start')
async def start(message: types.Message):
    start_button = ['Последняя игра', 'Игры и ело до цели']
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_button)
    
    await message.answer('Чо надо?', reply_markup=keyboard)

@dp.message_handler(Text(equals='Последняя игра'))
async def get_last_game(message:types.Message):
    await message.answer('Собираю информацию...')

    get_stats()

    with open(f'{CACHE_PATH}/data.json', 'r') as f:
        data = json.load(f)

    item = data[0]
    card = f"{hlink(item.get('Date'), item.get('link'))}\n" \
        f"{hbold('Карта: ')} {item.get('Map')}\n" \
        f"{hbold('Исход: ')} {item.get('Outcome')}\n" \
        f"{hbold('Счет: ')} {item.get('Score')}\n" \
        f"{hbold('Новое ело: ')} {item.get('new_elo')}\n" \
        f"{hbold('Ид матча: ')} {item.get('matchID')}\n" \
        f"{hbold('Киллы: ')} {item.get('kill')}\n" \
        f"{hbold('Смерти: ')} {item.get('death')}\n" \
        f"{hbold('К/Д: ')} {item.get('k/d')}\n" \
        f"{hbold('ХС %: ')} {item.get('hsp')}\n" \
    
    await message.answer(card, disable_web_page_preview=True)
    
    with open(f'{CACHE_PATH}/data.json', 'w') as f:
        f.close()
@dp.message_handler(Text(equals='Игры и ело до цели'))
async def elo(message: types.Message):
    await message.answer('Собираю информацию...')

    get_stats()

    with open(f'{CACHE_PATH}/data.json', 'r') as f:
        data = json.load(f)
        item = data[0]
        elo_now = int(item['new_elo'])

        difference = TARGET_ELO - elo_now
        games = round(difference/25)
        await message.answer(f'Осталось до конца цели {hbold(difference)} elo, примерно {hbold(games)} побед')
        await message.answer(f'При учете в 2 победы в день, осталось {hbold(int(games/2))} дней')


def main():
    executor.start_polling(dp)

if __name__ == '__main__':
    main()