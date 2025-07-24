import random
import logging
import os 
from pathlib import Path
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove,FSInputFile


# Конфигурация
BOT_TOKEN = "7604459732:AAE49WdblJZh_GyspEfJetWLm-PZUv1vRBI" 
CHANNEL_ID = "@tgksample"   

# Инициализация объектов
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

HARDCODED_TEXT = "Гоугоу на стрим!\nhttps://www.twitch.tv/zombyaak_doto"
HARDCODED_PHOTO_URL_MASSIVE = ['https://i.pinimg.com/736x/cc/34/7d/cc347d12e404f89e0320d40722a81725.jpg',
                       'https://i.pinimg.com/1200x/4f/eb/17/4feb17bad5cd72657ea01ea0636af713.jpg',
                       'https://i.pinimg.com/736x/5e/8c/51/5e8c51327816359990e7d9bc9c529ca4.jpg',
                       'https://i.pinimg.com/736x/c4/92/74/c49274ba06f2bcaee5fe504b43debfa5.jpg',
                       'https://i.pinimg.com/736x/98/aa/82/98aa82435e568d15da5b44014ee90277.jpg',
                       'https://i.pinimg.com/736x/2a/c9/e2/2ac9e290f5489685c3f0ee6be622c4a9.jpg',
                       'https://i.pinimg.com/736x/aa/35/da/aa35daabfaf98d226dfc4fc5837b4ddd.jpg',
                       'https://i.pinimg.com/736x/a5/23/55/a523557349e5c395c5f9001a5ddb6b81.jpg',
                       'https://i.pinimg.com/736x/43/fb/8d/43fb8d33570cc10d25fe29449c234722.jpg',
                       'https://i.pinimg.com/736x/df/e9/07/dfe9073768c1fa153d47a5ac12954407.jpg',
                       'https://i.pinimg.com/736x/c6/07/91/c607915536f831181a797a916f34a5f7.jpg',
                       'https://i.pinimg.com/736x/e0/ae/14/e0ae14fb8fef9aeef6b6373985242fa4.jpg',
                       'https://i.pinimg.com/736x/d6/6f/3c/d66f3c656d061ff8b62ecba19448af8c.jpg',
                       'https://i.pinimg.com/736x/7f/72/c7/7f72c7ef31a2fc34d55d0d5ea514a242.jpg',
                       'https://i.pinimg.com/736x/56/44/54/564454677a5a35b28be0ac2b3fd8e2ad.jpg',
                       'https://i.pinimg.com/736x/f6/39/80/f63980cbd1f3284cce781eee7e050076.jpg',
                       'https://i.pinimg.com/736x/e9/48/f4/e948f43b8a000b1aae3c6f1e88fdd4cc.jpg',
                       'https://i.pinimg.com/736x/2a/b0/57/2ab057f4c2b62828c0ad110f77d02628.jpg']
PHOTO_DIR = Path('C:/Users/eshkere/Documents/python/tg_bots/telegram-zombyak/media/photos')
CUSTOM_TEXT = "Гоугоу на стрим!\nhttps://www.twitch.tv/zombyaak_doto"





# Инициализация бота
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Состояния FSM
class Form(StatesGroup):
    waiting_for_text = State()
    waiting_for_photo = State()
    custom_photo = State()
    custom_text = State()

# Главное меню с 3 кнопками
main_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Дефолт сообщение")],
        [KeyboardButton(text="Свой текст и дефолтная фотка")],
        [KeyboardButton(text="Дефолт текст и своё фото")],
        [KeyboardButton(text="Всё свое")],
        [KeyboardButton(text="pidor")],
        [KeyboardButton(text="Отменить")]
    ],
    resize_keyboard=True
)

def update_photo(HARDCODED_PHOTO_URL_MASSIVE):
    HARDCODED_PHOTO_URL = random.choice(HARDCODED_PHOTO_URL_MASSIVE)
    return HARDCODED_PHOTO_URL
def get_random_photo():
    """Возвращает путь к случайному фото из папки"""
    if not PHOTO_DIR.exists():
        return None
    
    photos = []
    # Правильное использование os.walk()
    for root, _, files in os.walk(str(PHOTO_DIR)):  # Преобразуем Path в строку
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                photos.append(Path(root) / file)
    
    return random.choice(photos) if photos else None



# Обработчик /start
@dp.message(Command("start"))
async def start_command(message: types.Message):
    await message.answer(
        "Выбери тип отправки:",
        reply_markup=main_keyboard
    )

@dp.message(lambda message: message.text == "pidor")
async def pidor(message:types.Message):
    a = -1
    await message.answer("Пошел спам")
    words = ['заходите','сук','на','стрим','https://www.twitch.tv/zombyaak_doto']
    while a < len(words)-1:
        a+=1
        await bot.send_message(
            chat_id=CHANNEL_ID,
            text=words[a]
        )
        await asyncio.sleep(1)
    if a >= len(words)-1 :
        await message.answer("Дело сделано")
@dp.message(lambda message: message.text == "Дефолт сообщение")
async def send_hardcoded_with_photo(message: types.Message):
    photo_path = get_random_photo()
    try:
        await bot.send_photo(
            chat_id=CHANNEL_ID,
            photo=FSInputFile(photo_path),
            caption=HARDCODED_TEXT
        )
        
        await message.answer("Доставил")
    except Exception as e:
        await message.answer(f"❌ Ошибка: {str(e)}")

# Кнопка 2: Пользовательский текст + стандартное фото
@dp.message(lambda message: message.text == "Свой текст и дефолтная фотка")
async def request_custom_text(message: types.Message, state: FSMContext):
    await message.answer(
        "Сообщение вводи:",
        reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(Form.waiting_for_text)

#тут для кнопочки всё свое
@dp.message(lambda message: message.text == "Всё свое")
async def custom_text_photo(message: types.Message , state : FSMContext):
    await message.answer(
        "Сообщение введи",
        reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(Form.custom_text)


@dp.message(Form.custom_text)
async def process_custom_text(message: types.Message, state : FSMContext):
    await state.update_data(custom_text=message.text)
    await message.answer("Дай фотку")
    await state.set_state(Form.custom_photo)

@dp.message(Form.custom_photo)
async def process_custom_photo(message: types.Message, state: FSMContext):
    try:
        if not message.photo:
            await message.answer("Где фото чувак")
            return
        photo_file_id = message.photo[-1].file_id
        data = await state.get_data()
        custom_text = data.get('custom_text','')
        await bot.send_photo(
            chat_id=CHANNEL_ID,
            photo=photo_file_id,
            caption=f"{custom_text}\nhttps://www.twitch.tv/zombyaak_doto"
        )
        await message.answer(
            'Дело сделано',
            reply_markup=main_keyboard
        )
    except Exception as e:
        await message.answer(
            f'Что-то пошло не так лови лог ошибки \n {e}',
            reply_markup=main_keyboard
        )
    finally:
        await state.clear()

@dp.message(Form.waiting_for_text)
async def send_custom_text_with_photo(message: types.Message, state: FSMContext):
    photo_path = get_random_photo()
    try:

        await bot.send_photo(
            chat_id=CHANNEL_ID,
            photo=FSInputFile(photo_path),
            caption=f"{message.text}\nhttps://www.twitch.tv/zombyaak_doto"
        )
        await message.answer(
            "Дело сделано",
            reply_markup=main_keyboard
        )
    except Exception as e:
        await message.answer(
            f"❌ Ошибка: {str(e)}",
            reply_markup=main_keyboard
        )
    finally:
        await state.clear()

@dp.message(lambda message: message.text == "Дефолт текст и своё фото")
async def request_custom_photo(message: types.Message, state: FSMContext):
    await message.answer(
        "Отправь фото:",
        reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(Form.waiting_for_photo)


@dp.message(Form.waiting_for_photo)
async def send_hardcoded_text_with_photo(message: types.Message, state: FSMContext):
    try:

        if message.photo:

            photo_file_id = message.photo[-1].file_id
            
            
            await bot.send_photo(
                chat_id=CHANNEL_ID,
                photo=photo_file_id,
                caption=f'{CUSTOM_TEXT} '
            )
            await message.answer(
                "Дело сделано",
                reply_markup=main_keyboard
            )
        else:
            await message.answer(
                "Ты отправил не фото. Попробуй еще раз.",
                reply_markup=main_keyboard
            )
    except Exception as e:
        await message.answer(
            f"Ошибка: {str(e)}",
            reply_markup=main_keyboard
        )
    finally:
        await state.clear()

# Обработчик отмены
@dp.message(lambda message: message.text == "Отменить")
async def cancel_action(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state:
        await state.clear()
    await message.answer(
        "Действие отменено",
        reply_markup=main_keyboard
    )

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())