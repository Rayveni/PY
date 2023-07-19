from aiogram import  Dispatcher,F
from aiogram.types import Message
from emoji import emojize
from aiogram.utils.markdown import text, bold, italic, code, pre
from aiogram.fsm.context import FSMContext
from .text_templates import message_templates
from aiogram.filters import StateFilter
from aiogram.fsm.state import default_state
from aiogram.filters.command import Command
from .keyboards  import *
from .states import *

def setup_message_handlers(dispatcher:Dispatcher)->None:
    dispatcher.message.register(send_welcome,Command(commands=['start', 'about']),StateFilter(default_state))
    dispatcher.message.register(cmd_start,Command(commands=['start2']))
    dispatcher.message.register(process_command_2,Command(commands=['2']))
    dispatcher.message.register(cmd_start2,Command(commands=['start3']))   
    dispatcher.message.register(cmd_start3,Command(commands=['start4']))     
    dispatcher.message.register(cmd_goods,Command(commands=['goods']))
    dispatcher.message.register(process_cancel_command,Command(commands=['cancel']),StateFilter(default_state))    
    dispatcher.message.register(process_cancel_command_state,Command(commands=['cancel']),~StateFilter(default_state))      
      
    dispatcher.message.register(process_fillform_command,Command(commands=['fillform']),StateFilter(default_state)) 
    dispatcher.message.register(process_name_sent,StateFilter(FSMFillForm.fill_name), F.text.isalpha()) 
    dispatcher.message.register(warning_not_name,StateFilter(FSMFillForm.fill_name))     
    dispatcher.message.register(process_age_sent,StateFilter(FSMFillForm.fill_age),lambda x: x.text.isdigit() and 4 <= int(x.text) <= 120)        
    dispatcher.message.register(warning_not_age,StateFilter(FSMFillForm.fill_age))  
    dispatcher.message.register(warning_not_gender,StateFilter(FSMFillForm.fill_gender)) 


async def process_command_2(message: Message):
    await message.reply("Отправляю все возможные кнопки",
                        reply_markup=inline_kb())

async def send_welcome(message: Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    await message.reply(f"Hi!\nI'm EchoBott!{message.from_user.first_name}", parse_mode="HTML")
    
async def echo(message: Message):
    message_text = text(emojize('привет :thumbs_up: \n'),
                        italic('Я просто напомню'), ',что есть',
                        code('команда'), '/help')
    await message.reply(message_text, parse_mode="MarkdownV2")
    
async def cmd_start(message: Message):
    message_text = text(emojize('привет :thumbs_up: \n'),
                        italic('Я просто напомню'), ',что есть',
                        code('команда'), '/help')
    await message.answer(message_text, reply_markup=reply_kb())

async def cmd_start2(message: Message):
    message_text = message_templates['greet'].format(name=message.from_user.full_name)
    await message.answer(message_text, reply_markup=new_menu())
    
async def cmd_start3(message: Message):
    message_text = message_templates['greet'].format(name=message.from_user.full_name)
    await message.answer(message_text, reply_markup=pagination_kb('backward','11/380','444','forward'), parse_mode="HTML")
    
    
async def cmd_goods(message: Message):
    message_text = "goods keyboard"
    await message.answer(message_text, reply_markup=goods_kb())    
    


async def process_cancel_command_state(message: Message, state: FSMContext):
    await message.answer(text='Вы вышли из машины состояний\n\n'
                              'Чтобы снова перейти к заполнению анкеты - '
                              'отправьте команду /fillform')
    # Сбрасываем состояние
    await state.clear()


# Этот хэндлер будет срабатывать на команду "/cancel" в состоянии
# по умолчанию и сообщать, что эта команда доступна в машине состояний

async def process_cancel_command(message: Message, state: FSMContext):
    await message.answer(text='Отменять нечего. Вы вне машины состояний\n\n'
                              'Чтобы перейти к заполнению анкеты - '
                              'отправьте команду /fillform')
        # Сбрасываем состояние
    await state.clear()
    
    
# Этот хэндлер будет срабатывать на команду /fillform
# и переводить бота в состояние ожидания ввода имени

async def process_fillform_command(message: Message, state: FSMContext):
    await message.answer(text='Пожалуйста, введите ваше имя')
    # Устанавливаем состояние ожидания ввода имени
    await state.set_state(FSMFillForm.fill_name)


# Этот хэндлер будет срабатывать, если введено корректное имя
# и переводить в состояние ожидания ввода возраста

async def process_name_sent(message: Message, state: FSMContext):
    # Cохраняем введенное имя в хранилище по ключу "name"
    await state.update_data(name=message.text)
    await message.answer(text='Спасибо!\n\nА теперь введите ваш возраст')
    # Устанавливаем состояние ожидания ввода возраста
    await state.set_state(FSMFillForm.fill_age)


# Этот хэндлер будет срабатывать, если во время ввода имени
# будет введено что-то некорректное

async def warning_not_name(message: Message):
    await message.answer(text='То, что вы отправили не похоже на имя\n\n'
                              'Пожалуйста, введите ваше имя\n\n'
                              'Если вы хотите прервать заполнение анкеты - '
                              'отправьте команду /cancel')


# Этот хэндлер будет срабатывать, если введен корректный возраст
# и переводить в состояние выбора пола


async def process_age_sent(message: Message, state: FSMContext):
    # Cохраняем возраст в хранилище по ключу "age"
    await state.update_data(age=message.text)
    # Создаем объекты инлайн-кнопок
    male_button = InlineKeyboardButton(text='Мужской ♂',
                                       callback_data='male')
    female_button = InlineKeyboardButton(text='Женский ♀',
                                         callback_data='female')
    undefined_button = InlineKeyboardButton(text='🤷 Пока не ясно',
                                            callback_data='undefined_gender')
    # Добавляем кнопки в клавиатуру (две в одном ряду и одну в другом)
    keyboard: list[list[InlineKeyboardButton]] = [[male_button, female_button],
                                                  [undefined_button]]
    # Создаем объект инлайн-клавиатуры
    markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
    # Отправляем пользователю сообщение с клавиатурой
    await message.answer(text='Спасибо!\n\nУкажите ваш пол',
                         reply_markup=markup)
    # Устанавливаем состояние ожидания выбора пола
    await state.set_state(FSMFillForm.fill_gender)


# Этот хэндлер будет срабатывать, если во время ввода возраста
# будет введено что-то некорректное

async def warning_not_age(message: Message):
    await message.answer(
        text='Возраст должен быть целым числом от 4 до 120\n\n'
             'Попробуйте еще раз\n\nЕсли вы хотите прервать '
             'заполнение анкеты - отправьте команду /cancel')





# Этот хэндлер будет срабатывать, если во время выбора пола
# будет введено/отправлено что-то некорректное

async def warning_not_gender(message: Message):
    await message.answer(text='Пожалуйста, пользуйтесь кнопками '
                              'при выборе пола\n\nЕсли вы хотите прервать '
                              'заполнение анкеты - отправьте команду /cancel')





