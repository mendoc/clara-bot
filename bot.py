import logging
import os
from dotenv import load_dotenv
from chatutils import generate_response
from telegram import Update
from telegram.ext import filters, ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler


# Chargement des variables d'environemment du fichier .env
load_dotenv()

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


def save_prompt(file_name: str, message: str):
    fichier = open(f"{file_name}.txt", "a")
    fichier.write(message + "\n")
    fichier.close()


def get_prompt(file_name: str):
    fichier = open(f"{file_name}.txt", "r")
    p = fichier.read()
    fichier.close()

    return p


async def init_prompt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    fichier = open(f"{update.message.chat.id}.txt", "w")
    fichier.close()

    await context.bot.send_message(chat_id=update.effective_chat.id, text="Conversation reinitialisée")


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    save_prompt(update.message.chat.id, "user: " + update.message.text + "[stop]")
    prompt = get_prompt(update.message.chat.id) + "\nassistant:"
    response = generate_response(prompt)
    save_prompt(update.message.chat.id, "assistant:" + response + "[stop]")
    await context.bot.send_message(chat_id=update.effective_chat.id, text=response)


if __name__ == '__main__':
    application = ApplicationBuilder().token(os.getenv("BOT_TOKEN")).build()

    start_handler = CommandHandler('start', init_prompt)
    new_handler = CommandHandler('new', init_prompt)
    echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)

    application.add_handler(start_handler)
    application.add_handler(echo_handler)
    application.add_handler(new_handler)

    application.run_polling()
