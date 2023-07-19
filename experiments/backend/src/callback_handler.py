from aiogram import Dispatcher
from aiogram.types import CallbackQuery
from aiogram.filters import StateFilter,Text
from aiogram.fsm.context import FSMContext
from .keyboards  import pagination_kb
from .filters import *
from .states import *

def setup_callback_handler(dispatcher:Dispatcher)->None:
    dispatcher.callback_query.register(process_callback_button1,lambda c: c.data == 'button1')  
    dispatcher.callback_query.register(process_pagination,lambda c: c.data in  ('forward','backward'))  
    dispatcher.callback_query.register(goods,GoodsCallbackFactory.filter())  
    dispatcher.callback_query.register(process_callback_kb1btn1)    
    
    dispatcher.callback_query.register(process_gender_press,StateFilter(FSMFillForm.fill_gender),Text(text=['male', 'female', 'undefined_gender']))  
async def process_callback_kb1btn1(callback_query: CallbackQuery):
    code = callback_query.data[-1]
    if code.isdigit():
        code = int(code)
    if code == 2:
        await callback_query.message.answer( text='Нажата вторая кнопка')
    elif code == 5:
        await callback_query.answer(
            text='Нажата кнопка с номером 5.\nА этот текст может быть длиной до 200 символов 😉',
            show_alert=True)
    else:
        print(callback_query.json(indent=4, exclude_none=True))
        await callback_query.message.answer(str(callback_query.json(indent=4, exclude_none=True)))
    #await bot.send_message(callback_query.from_user.id, f'Нажата инлайн кнопка! code={code}')
    await callback_query.message.answer(callback_query)
    
    
async def process_callback_button1(callback_query: CallbackQuery):
    await callback_query.message.answer("Итого:1")
    await callback_query.answer(text= "Нажата первая кнопка!")

page=10    
async def process_pagination(callback_query: CallbackQuery):
    global page
    if callback_query.data=='forward':
        page=page+1
    else:
        page=page-1
    _keyboard=pagination_kb('backward',f'{page}/400','forward')
    await callback_query.message.edit_text(text='dddw',reply_markup=_keyboard)


async def goods(callback_query: CallbackQuery):
    await callback_query.message.edit_text(text='test filter goods')

# Этот хэндлер будет срабатывать на нажатие кнопки при
# выборе пола и переводить в состояние отправки фото

async def process_gender_press(callback: CallbackQuery, state: FSMContext):
    # Cохраняем пол (callback.data нажатой кнопки) в хранилище,
    # по ключу "gender"
    await state.update_data(gender=callback.data)
    # Удаляем сообщение с кнопками, потому что следующий этап - загрузка фото
    # чтобы у пользователя не было желания тыкать кнопки
    await callback.message.delete()
    await callback.message.answer(text='Спасибо! А теперь загрузите, '
                                       'пожалуйста, ваше фото')
    # Устанавливаем состояние ожидания загрузки фото
    await state.set_state(FSMFillForm.upload_photo)