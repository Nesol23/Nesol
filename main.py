import telebot
import os
import random
import requests

bot = telebot.TeleBot("7031381945:AAGXys9ZCrDRJqJONcErzP4OZdMA9v5bwzA")

def get_cat_image_url():
    url = 'https://api.thecatapi.com/v1/images/search'
    try:
        res = requests.get(url)
        res.raise_for_status()
        data = res.json()
        return data[0]['url']
    except requests.exceptions.RequestException as e:
        return f"Error fetching cat image: {e}"

def get_duck_image_url():
    # REPLACE THIS WITH A REAL API CALL TO FETCH A DUCK IMAGE URL
    # Example (replace with your actual API):
    # url = "https://some-duck-api.com/images"
    # try:
    #     res = requests.get(url)
    #     res.raise_for_status()
    #     data = res.json()
    #     return data[0]['url']
    # except requests.exceptions.RequestException as e:
    #     return f"Error fetching duck image: {e}"
    return "https://upload.wikimedia.org/wikipedia/commons/thumb/4/48/Mallard_Hen_001.jpg/1280px-Mallard_Hen_001.jpg" # Placeholder


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Я твой Telegram бот. Используй /mem для мема, /duck для утки или /cat для котика.")

@bot.message_handler(commands=['mem'])
def send_mem(message):
    images_dir = "images"
    try:
        image_files = [f for f in os.listdir(images_dir) if os.path.isfile(os.path.join(images_dir, f))]
        if not image_files:
            bot.reply_to(message, "Извини, в папке с мемами нет файлов.")
            return

        random_image = random.choice(image_files)
        image_path = os.path.join(images_dir, random_image)
        with open(image_path, 'rb') as f:
            bot.send_photo(message.chat.id, f)
    except FileNotFoundError:
        bot.reply_to(message, "Извини, папка с мемами не найдена.")
    except Exception as e:
        bot.reply_to(message, f"Произошла ошибка: {e}")

@bot.message_handler(commands=['duck'])
def duck(message):
    image_url = get_duck_image_url()
    bot.reply_to(message, image_url)

@bot.message_handler(commands=['cat'])
def cat(message):
    image_url = get_cat_image_url()
    bot.reply_to(message, image_url)

bot.polling()