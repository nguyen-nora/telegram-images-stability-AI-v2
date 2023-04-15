# Commented out IPython magic to ensure Python compatibility.
#%pip install ..
# %pip install stability-sdk
# %pip install nest-asyncio
# %pip install transformers
# %pip install diffusers
# %pip install python-telegram-bot
# %pip install accelerate
# %pip install pyTelegramBotAPI

## Add API

import getpass, os

# NB: host url is not prepended with \"https\" nor does it have a trailing slash.
os.environ['STABILITY_HOST'] = 'grpc.stability.ai:443'

# To get your API key, visit https://beta.dreamstudio.ai/membership
os.environ['STABILITY_KEY'] = 'Enter your API Key' #Add API key here

import io
import os
import warnings

from IPython.display import display
from PIL import Image
from stability_sdk import client
import stability_sdk.interfaces.gooseai.generation.generation_pb2 as generation


stability_api = client.StabilityInference(
    key=os.environ['STABILITY_KEY'], 
    verbose=True,
)

##----------------------------------------------------------------##

from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
import telebot
from telebot import TeleBot
BOT_TOKEN='Enter your API Telegram bot'#Add Token Telegram bot
bot=TeleBot(BOT_TOKEN)
# First command
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Xin chào! Tôi là bot AI của bạn. Hãy đặt câu hỏi của bạn và tôi sẽ cố gắng trả lời cho bạn.")
@bot.message_handler(commands=['genimages'])
def send_images(message):
    ## Text to images
    # Retrieve user's messages
    textimg = message.text
    delimiter = " "
    split = textimg.split(delimiter, 1)[1]
    # Create API Stability
    answers = stability_api.generate(
        prompt = split,
        seed=34567, # if provided, specifying a random seed makes results deterministic
        steps=60, # defaults to 30 if not specified
    )
    # Run API
    warningtext = "Yêu cầu của bạn đã kích hoạt bộ lọc an toàn của API và không thể được xử lý. Vui lòng thử lại sau!"
    for resp in answers:
        for artifact in resp.artifacts:
            if artifact.finish_reason == generation.FILTER:
                bot.reply_to(message, warningtext)
            if artifact.type == generation.ARTIFACT_IMAGE:
                img = Image.open(io.BytesIO(artifact.binary))
                bot.send_photo(message.chat.id, photo=img)

#Run bot
bot.polling()
