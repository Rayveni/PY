import logging
from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand

#from aiogram.dispatcher.middlewares.logging import LoggingMiddleware
from os import getenv

from .text_templates import command_menu


async def setup_bot_commands(dispatcher:Dispatcher):
    main_menu_commands = [BotCommand(
                                command=command,
                                description=description
                          ) for command,
                                description in command_menu.items()]
    await dispatcher.bot.set_my_commands(main_menu_commands)
    
def bot_init():
    API_TOKEN = getenv('tg_secret')
    log_dir,log_level= getenv('app_logs'),getenv('log_level','INFO').upper()
    # Configure logging
    logging.basicConfig(format=u'%(filename)+13s [ LINE:%(lineno)-4s] %(levelname)-8s [%(asctime)s] %(message)s',
                        level=log_level,
                        filename=f"{log_dir}/app.log",filemode="a")
    
    logger = logging.getLogger('app_logger')
    # Initialize bot and dispatcher
    bot = Bot(token=API_TOKEN, parse_mode="HTML")#MarkdownV2
    dp=Dispatcher()
    #dp.middleware.setup(LoggingMiddleware())
    return bot,dp,logger