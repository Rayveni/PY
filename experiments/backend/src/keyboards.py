from aiogram.types import ReplyKeyboardRemove,ReplyKeyboardMarkup, KeyboardButton,InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from .text_templates import pagination
from .filters import *

def reply_kb():
    button1 = KeyboardButton(text='1️⃣')
    button2 = KeyboardButton(text='2️⃣')
    button3 = KeyboardButton(text='3️⃣')

  

    button4 = KeyboardButton(text='4️⃣')
    button5 = KeyboardButton(text='5️⃣')
    button6 = KeyboardButton(text='6️⃣')


    markup5 = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True ,keyboard=[[button1, button2,button3],[button4],[button5,button6]])
    return markup5

def inline_kb():
    inline_btn_1 = InlineKeyboardButton(text='Первая кнопка!', callback_data='button1')

    inline_btn_2= InlineKeyboardButton(text='Вторая кнопка', callback_data='btn2')
    inline_btn_3 = InlineKeyboardButton(text='кнопка 3', callback_data='btn3')
    inline_btn_4 = InlineKeyboardButton(text='кнопка 4', callback_data='btn4')
    inline_btn_5 = InlineKeyboardButton(text='кнопка 5', callback_data='btn5')

    inline_btn_6 =InlineKeyboardButton(text="query=''", switch_inline_query='')
    inline_btn_7 =InlineKeyboardButton(text="query='qwerty'", switch_inline_query='qwerty')
    inline_btn_8 =InlineKeyboardButton(text="Inline в этом же чате", switch_inline_query_current_chat='wasd')
    inline_btn_9 =InlineKeyboardButton(text='Уроки aiogram', url='https://surik00.gitbooks.io/aiogram-lessons/content/')
    
    inline_keyboard=[[inline_btn_1,inline_btn_2],[inline_btn_3, inline_btn_4, inline_btn_5],[inline_btn_6,inline_btn_7],[inline_btn_8],[inline_btn_9]]
    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)



def new_menu():
    menu_btn = [
        [InlineKeyboardButton(text="📝 Генерировать текст", callback_data="generate_text"),
        InlineKeyboardButton(text="🖼 Генерировать изображение", callback_data="generate_image")],
        [InlineKeyboardButton(text="💳 Купить токены", callback_data="buy_tokens"),
        InlineKeyboardButton(text="💰 Баланс", callback_data="balance")],
        [InlineKeyboardButton(text="💎 Партнёрская программа", callback_data="ref"),
        InlineKeyboardButton(text="🎁 Бесплатные токены", callback_data="free_tokens")],
        [InlineKeyboardButton(text="🔎 Помощь", callback_data="help")]
    ]
    menu = InlineKeyboardMarkup(inline_keyboard=menu_btn)
    return menu



def pagination_kb(*buttons: str) -> InlineKeyboardMarkup:
    # Инициализируем билдер
    kb_builder=InlineKeyboardBuilder()
    # Добавляем в билдер ряд с кнопками
    kb_builder.row(*[InlineKeyboardButton(
        text=pagination[button] if button in pagination else button,
        callback_data=button) for button in buttons])
    # Возвращаем объект инлайн-клавиатуры
    return kb_builder.as_markup()

def goods_kb():
    button_1: InlineKeyboardButton = InlineKeyboardButton(
                    text='Категория 1',
                    callback_data=GoodsCallbackFactory(
                                            category_id=1,
                                            subcategory_id=0,
                                            item_id=0).pack())

    button_2: InlineKeyboardButton = InlineKeyboardButton(
                        text='Категория 2',
                        callback_data=GoodsCallbackFactory(
                                                category_id=2,
                                                subcategory_id=0,
                                                item_id=0).pack())

    return InlineKeyboardMarkup(inline_keyboard=[[button_1,button_2]],row_width=2)

