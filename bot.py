import os
import aiogram.utils.markdown as fmt
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.utils import executor
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from aiogram.types import \
    InlineKeyboardMarkup, InlineKeyboardButton
#from aiogram.utils.emoji import emojize
from aiogram.utils.markdown import text, bold, italic, code, pre
import web
from config import TOKEN, DB_FILENAME
from db_facs_map import Base, Facs, Groups
from utils import States

bot = Bot(token=TOKEN)
dp = Dispatcher(bot,storage=MemoryStorage())
engine = create_engine(f'sqlite:///{DB_FILENAME}')

Base.metadata.create_all(engine)

session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)
session = Session()
@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await message.reply("Здравствуйте! \nВыберите команду")

@dp.message_handler(commands=['help'])
async def help_command(message: types.Message):
    await message.reply("Я бот в бета разработке. Вот, что я пока могу: \n ") #ДоРаБоТаТь

@dp.message_handler(commands=['group'])
async def select_group(message: types.Message):
    msg = 'Ваша группа: '+message.text
    await bot.send_message(msg.from_user.id,msg) #ДоРаБоТаТь

@dp.message_handler(commands=['facs'])
async def select_fac(message: types.Message,  state: FSMContext):
    inline_kb = InlineKeyboardMarkup()
    inline_kb.row_width = 1
    for f in await web.get_Facs():
        f_n = Facs(fac_id=f[0],
                   fac_name=f[1])
        session.add(f_n)
        session.commit()
        inline_kb.add(InlineKeyboardButton(f[1], callback_data=f[0]))
        print(f[1])
    await state.set_state(States.SETTED_FAC)
    await message.reply('Выберите свой факультет:',reply_markup=inline_kb) #ДоРаБоТаТь

@dp.callback_query_handler(state=States.SETTED_FAC)
async def callback_fac(call,state: FSMContext):
   # if call.data == 'dog':
    inline_kb = InlineKeyboardMarkup()
    inline_kb.row_width = 1
    grps = web.get_Groups(call.data)
    for g in await grps:
        g_n = Groups(group_name=g,
                    fac_id=call.data)
        session.add(g_n)
        session.commit()
        inline_kb.add(InlineKeyboardButton(g, callback_data=g))
        print(g)
    await state.set_state(States.SETTED_GROUP)
    await bot.send_message(call.message.chat.id, 'Теперь выберите группу', reply_markup=inline_kb)

@dp.callback_query_handler(state=States.SETTED_GROUP)
async def callback_group(call,state: FSMContext):
    table = await web.get_Table(session.query(Groups).filter(Groups.group_name == call.data).first().fac_id, call.data)
    msg = ''
    for w in table.keys():
        msg+='<strong>--------------'+w+'--------------\n</strong>'
        for d in table[w].keys():
            msg+='<u>'+d+'----------------------</u>\n'
            if table[w][d]['lesson']:
                for l in table[w][d]['lesson']:
                    msg+='<b>       '+l['time']+'</b> '
                    msg+=l['room']
                    msg+=''+l['name']+'\n'
                    msg+='<i>       '+l['tutor']+'</i>\n\n'
            else:
                msg+='<a>Занятий нет\n</a>'
            msg+='<a>\n</a>'
    await bot.send_message(call.message.chat.id,msg, parse_mode="HTML") #<a href="URI_адрес">Анкор ссылки</a>, <b>, <strong>, <i> and <em>.
    await state.reset_state()



if __name__ == '__main__':
    executor.start_polling(dp)