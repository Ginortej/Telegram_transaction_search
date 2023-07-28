from aiogram import Bot, Dispatcher, executor, types
from tockin import *
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from sql_requests_1 import Requests
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import socket





# 
bot = TOCKIN
bot_main = Bot(bot)
dp = Dispatcher(bot_main, storage=MemoryStorage())
req_sql = Requests()
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT,))



# класс для выстовления состояний бота с помощю которых можно будет добовлять функционал боту 
class State(StatesGroup):
    st0 = State()
    st1 = State()
    st2 = State()
    st3 = State()
    st4 = State()



# HOST = "127.0.0.1"  
# PORT = 65432  # The port used by the server

# sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# sock.connect((HOST, PORT,))


# функция для отправления на серевер сообщения 
def trans(data:str):
        global sock
        sock.send(bytes(data.encode('utf-8')))
        return sock.recv(1024)    


# функция с которой идет запуск бота что бы запустить бота надо отправить /start функция создает клавиатуру в чате с пользователем так же проверяет есть ли данные о данном пользователе а конкретно айди чата и имя пользователя 
# после чего перекидывает на стотояние 0  
@dp.message_handler(commands= ['start'], state= None)
async def starting(message: types.Message):
    global req_sql
    makup = types.ReplyKeyboardMarkup()
    butn0 = types.KeyboardButton('отслеживание')
    butn1 = types.KeyboardButton('удалить отслеживание')
    butn2 = types.KeyboardButton('за какими кошелками следишь')
    butn3 = types.KeyboardButton('Аналитика кошелька')
    makup.add(butn0, butn1, butn2)
    await message.answer(text='Привет нажми на кнопку отслеживание после чего напиши URL-ссылку кошелка который хочешь отслеживать \nТак же ты можешь посмотреть за какими кошельками следишь\n',reply_markup=makup)
    data_user   =  req_sql._look_id_chat()
    for usr in data_user:
        if usr == None:
            req_sql.new_users(message.chat.id,message.from_user.full_name)
        elif message.chat.id != usr:
            req_sql.new_users(message.chat.id,message.from_user.full_name)
        else:
            pass
    await State.st0.set()
    # await message.delete()
    


# В этой же функции идет обработка запросов от пользователя по нажитую кнопки после нажатия происходит переход на следущие состояние в завимости от нажатие кнопки 
@dp.message_handler(state= State.st0)
async def message_processing(message: types.Message, state: FSMContext):
    if message.text in 'отслеживание':
            await message.answer(text='Напиши URL-ссылку кошелка который хочешь отслеживать \nНо ссылка обязательно должна начинаться с 0x и так далее\nпример 0x4234df324')
            await State.st1.set()
    elif message.text in 'удалить отслеживание':
            await message.answer('пока что не сделал')
    elif message.text in 'за какими кошелками следишь':
            await message.answer('Отправь + для подтевржедения')
            await State.st2.set()

# состояние 1 эта функция отвечает за добовление новых кошельков 
@dp.message_handler(state= State.st1)
async def message_processing(message: types.Message, state: FSMContext):
    link = message.text
    if link[0:2] == '0x': # проверяем сообщение на то что это кошельек это давольно плохая проверка 
        reg = [True for i in req_sql._look_wallet(message.chat.id) if i == message.text] # здесь мы обращаемся к базе данных и через условия мы проверям есть ли такой же кошелек уже за которым следит сервер что бы не было повторений
        if reg: # проверяем повторение
            await message.answer('Вы его уже добавили')
        else:
            req_sql.new_wallet(message.text,message.chat.id)
            transacnions = trans(f'last {link}')
            await message.answer('Хорошо я запомнил вот последние транзакция этого кошелька')
            await message.answer(transacnions.decode())
            
        # transacnions_track = trans(f'full {link}')
    else:
        await message.answer('Это не ссылка чел')
    await State.st0.set() # возрощаем пользователя обратно в 0 стостояние для испоьзование меню


@dp.message_handler(state= State.st2)# состояние 2 в котором мы обращаемся к бызе данных смотрим какие кошельки сохранены функция форматирует данные и возрощает их 
async def message_processing(message: types.Message):
    try:
        ger = ''
        res  = req_sql._look_wallet(message.chat.id) # запрашиваем данные у sqllite 
        for i in res:  # перебераем список из кошельков
            ger += f"{i}\n"  # записываем все кошельки в одну переменную и с новой строки 
        await message.answer(ger)# выводим кошельки
    except:
        await message.answer('У тебя нет просматривающих кошельков')
    finally:
        await State.st0.set() # возрощаем пользователя обратно в 0 стостояние для испоьзование меню
    

@dp.message_handler(state= State.st3)
async def message_processing(message: types.Message):
    pass

@dp.message_handler(state= State.st4)
async def message_processing(message: types.Message):
    pass





if __name__ == '__main__':
    executor.start_polling(dp)










