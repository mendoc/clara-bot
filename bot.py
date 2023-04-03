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


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    save_prompt(update.message.chat.id, "Human: " + update.message.text)
    prompt = get_prompt(update.message.chat.id) + "\nAI:"
    response = generate_response(prompt)
    save_prompt(update.message.chat.id, "AI:" + response)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=response)


async def voice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    c_time = time()
    # get basic info about the voice note file and prepare it for downloading
    new_file = await context.bot.get_file(update.message.voice.file_id)
    # return
    # download the voice note as a file
    filename = f"{update.message.chat.id}.ogg"
    r = await new_file.download_to_drive(custom_path=filename)
    print(type(r), r)
    model = whisper.load_model("small")
    result = model.transcribe(filename, language="fr", fp16=False)
    trans = result["text"] + "\n\nTime: " + str(int(time() - c_time)) + " s."
    await context.bot.send_message(chat_id=update.effective_chat.id, text=trans)




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
