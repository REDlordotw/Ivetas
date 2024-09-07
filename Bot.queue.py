import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Привет! Используйте команду /join для добавления себя в очередь.')

async def join_queue(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.message.from_user
    if 'queue' not in context.bot_data:
        context.bot_data['queue'] = []
    
    if user.id not in context.bot_data['queue']:
        context.bot_data['queue'].append(user.id)
        await update.message.reply_text(f'Вы добавлены в очередь. Ваш номер: {len(context.bot_data["queue"])}')
    else:
        position = context.bot_data['queue'].index(user.id) + 1
        await update.message.reply_text(f'Вы уже в очереди. Ваш номер: {position}')

async def show_queue(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if 'queue' not in context.bot_data or not context.bot_data['queue']:
        await update.message.reply_text('Очередь пуста.')
    else:
        message = "Очередь:\n"
        for index, user_id in enumerate(context.bot_data['queue']):
            message += f"{index + 1}. Пользователь ID: {user_id}\n"
        await update.message.reply_text(message)

async def leave_queue(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.message.from_user
    if 'queue' in context.bot_data and user.id in context.bot_data['queue']:
        context.bot_data['queue'].remove(user.id)
        await update.message.reply_text('Вы покинули очередь.')
    else:
        await update.message.reply_text('Вы не в очереди.')

def main() -> None:
    application = Application.builder().token('5798175443:AAE_2A7su1TpQQI2NfajFqU2QCW68b78XXE').build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("join", join_queue))
    application.add_handler(CommandHandler("show", show_queue))
    application.add_handler(CommandHandler("leave", leave_queue))

    application.run_polling()

if __name__ == '__main__':
    main()