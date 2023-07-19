from src.bot_init import bot_init,setup_bot_commands
from src.message_handlers import setup_message_handlers
from src.callback_handler import setup_callback_handler

bot, dp, logger = bot_init()
logger.info('bot started')

# add handlers
setup_message_handlers(dp)
setup_callback_handler(dp)
 
if __name__ == '__main__':
    dp.run_polling(bot, skip_updates=True, on_startup=setup_bot_commands)
