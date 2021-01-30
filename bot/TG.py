import config
import blackFON
import filterPIL
import os
import draw
import keyboards as kb
from aiogram import Bot, Dispatcher, executor, types
import logging
from sqlitecontrol import Sqlitecontrol
logging.basicConfig(level=logging.INFO)
bot = Bot(token=config.API_TOKEN)
dp = Dispatcher(bot)
db = Sqlitecontrol('TGBase.db')
#определение




@dp.callback_query_handler(lambda c: c.data and c.data.startswith('bt'))
async def process_callback_bt_cool(callback_query: types.CallbackQuery):
    code = callback_query.data[-1]
    await bot.answer_callback_query(callback_query.id)
    if code.isdigit():
        code = int(code)
    if db.obr_get(callback_query.from_user.id)==1:
        if code == 1:
            markup1 = types.ReplyKeyboardRemove()
            await bot.send_message(callback_query.from_user.id, 'Нажата крутая кнопка!')
            db.obr_set(callback_query.from_user.id, 0)
            db.like_set(callback_query.from_user.id, 1)
        elif code == 2:
            markup1 = types.ReplyKeyboardRemove()
            await bot.send_message(callback_query.from_user.id, 'Нажата грустная кнопка!')
            db.obr_set(callback_query.from_user.id, 0)
            db.like_set(callback_query.from_user.id, -1)
    else:
        await bot.send_message(callback_query.from_user.id, 'Асуждаю двойные нажатия!')





@dp.callback_query_handler(lambda c: c.data and c.data.startswith('c'))
async def process_callback_l(callback_query: types.CallbackQuery):
    code = callback_query.data[1:]
    await bot.answer_callback_query(callback_query.id)
    if db.status_get(callback_query.from_user.id) == 2:
        markup1 = types.ReplyKeyboardRemove()
        db.status_set(callback_query.from_user.id, 3)
        db.set_args(callback_query.from_user.id, 1, code)
        mas = db.get_args(callback_query.from_user.id)
        filterPIL.filter(str(callback_query.from_user.id) + '.jpg')
        draw.dr((str(callback_query.from_user.id) + '.jpg'), db.get_name(callback_query.from_user.id), mas)
        f = open(str(callback_query.from_user.id) + '.jpg', "rb")
        await Bot.send_photo(self=bot, chat_id=callback_query.from_user.id, photo=f)
        await bot.send_message(callback_query.from_user.id, 'ну как?', reply_markup=kb.greet_kb)
        db.obr_set(callback_query.from_user.id, 1)
        os.remove(str(callback_query.from_user.id) + '.jpg')
        # await bot.send_photo(message.from_user.id, im)
    else:
        await bot.send_message(callback_query.from_user.id, 'Асуждаю ненужные нажатия!')

@dp.callback_query_handler(lambda c: c.data and c.data.startswith('l'))
async def process_callback_c(callback_query: types.CallbackQuery):
    code = callback_query.data[1:]
    await bot.answer_callback_query(callback_query.id)
    if code == '2':
        await bot.send_message(callback_query.from_user.id, "введи размер подписи\n(0 если не нужна)\n(рекомендую 50)")
        db.status_set(callback_query.from_user.id, 1)
    elif code == '1':
        await bot.send_message(callback_query.from_user.id, "введи слово")
        db.status_set(callback_query.from_user.id, 10)


    #await bot.edit_message_reply_markup(callback_query.id, message_id = callback_query.message.message_id-1, reply_markup = '')

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    markdown = """
            *bold text*
            _italic text_
            [text](URL)
            """
    await message.answer("*Привет*. Я посмогу тебе создавать классные мемы _без всяких усилий._\n напиши мне своё имя для подписи.\n вот так: /set_name имя \nЗатем можете отправлять своё фото для мема\n напиши /my_rate для просмотра ваше рейтинга _оценки_ моей работы \n \n [мой канал](https://www.youtube.com/channel/UCMBxOvbDi8qN81yT8NmmeXw)", parse_mode="Markdown")

@dp.message_handler(commands=['my_rate'])
async def my_rate(message: types.Message):
    markdown = """
        *bold text*
        _italic text_
        [text](URL)
        """
    await message.answer(('_ваш счёт:_  *' + str(db.like_get(message.from_user.id)) + '*'),parse_mode="Markdown")

@dp.message_handler(commands=['help'])
async def help(message: types.Message):
    markdown = """
                *bold text*
                _italic text_
                [text](URL)
                """
    await message.answer("*Привет*. Я посмогу тебе создавать классные мемы _без всяких усилий._\n напиши мне своё имя для подписи.\n вот так: /set_name\n Затем можете отправлять своё фото для мема\n напиши /my_rate для просмотра ваше рейтинга _оценки_ моей работы \n \n [мой канал](https://www.youtube.com/channel/UCMBxOvbDi8qN81yT8NmmeXw)", parse_mode="Markdown")

@dp.message_handler(commands=['set_name'])
async def set_name(message: types.Message):
    print(message.from_user['id'])
    print(message.get_args())
    if message.get_args() == '' or None:
        await message.answer("эммм. Пусто как-бы!")
    elif(db.exists(message.from_user['id']) == None):
        db.add_name(tg_id=message.from_user['id'], name=message.get_args())
        await message.answer("я тебя запомню, можешь скинуть фото")
    else:
        await message.answer("эммм, я тебя и так знаю")

@dp.message_handler(content_types=['photo'])
async def photoes(message):
    await message.photo[-1].download(str(message.from_user['id'])+'.jpg')
    await message.answer("выбери режим:", reply_markup=kb.l_kb)

@dp.message_handler(content_types=['text'])
async def all_mess(message):
    if db.status_get(message.from_user['id']) == 1:
        try:
            it = int(message.text)
            await bot.send_message(message.from_user['id'], 'какой цвет подписи?', reply_markup=kb.c_kb)
            db.status_set(message.from_user['id'], 2)

            db.set_args(message.from_user['id'], 0,str(it))


        except Exception as exc:
            await bot.send_message(message.from_user['id'], 'может число введёшь ?')
            print(exc)
    if db.status_get(message.from_user['id']) == 10:

        it = (message.text)

        blackFON.r(str(message.from_user['id']) + '.jpg', it)
        f = open(str(message.from_user['id']) + '.jpg', "rb")
        await Bot.send_photo(self=bot, chat_id=message.from_user['id'], photo=f)
        os.remove(str(message.from_user['id']) + '.jpg')
        await bot.send_message(message.from_user['id'], 'ну как?', reply_markup=kb.greet_kb)
        db.obr_set(message.from_user['id'], 1)



if __name__ == '__main__':
    mode = 0
    if mode == 1:
        try:
            executor.start_polling(dp, skip_updates=True)
        except:
            pass
    else:
        executor.start_polling(dp, skip_updates=True)