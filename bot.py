import logging
import os
from dotenv import load_dotenv
from chatutils import generate_response
from telegram import Update
from telegram.ext import filters, ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler
import whisper
from time import time

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


async def send_response(chatid: str, message: str, context: ContextTypes.DEFAULT_TYPE):
    history = get_prompt(chatid)
    query = "Human: " + message + "\nAI:"
    response = generate_response(history + query)
    save_prompt(chatid, query + response)
    await context.bot.send_message(chat_id=chatid, text=response)


async def voice_to_text(file_name: str, lang: str="fr"):
    model = whisper.load_model("small")
    result = model.transcribe(file_name, language=lang, fp16=False)
    trans = result["text"]
    return trans


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await send_response(update.message.chat.id, update.message.text, context)
    

async def voice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Save voice message to the disk
    voice_file = await context.bot.get_file(update.message.voice.file_id)
    file_name = f"{update.message.chat.id}.ogg"
    await voice_file.download_to_drive(custom_path=file_name)

    # Transcribe voice to text
    trans = await voice_to_text(file_name)

    # Handle text with chatGPT and send response to user
    if len(trans) > 0:
        await send_response(update.message.chat.id, trans, context)


if __name__ == '__main__':
    application = ApplicationBuilder().token(os.getenv("BOT_TOKEN")).build()

    start_handler = CommandHandler('start', init_prompt)
    new_handler   = CommandHandler('new', init_prompt)
    echo_handler  = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)
    voice_handler = MessageHandler(filters.VOICE & (~filters.COMMAND), voice)

    application.add_handler(start_handler)
    application.add_handler(echo_handler)
    application.add_handler(voice_handler)
    application.add_handler(new_handler)

    application.run_polling()
