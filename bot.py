import telebot
import os
from datetime import datetime

# Token endi serverdan olinadi (Render yoki boshqa serverdan)
TOKEN = os.environ.get("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

# Ishchilar ma'lumotlari
workers = {}

# 📊 Yordamchi funksiya (hisobot chiqarish)
def get_report(worker):
    day = workers[worker]["today"]
    week = workers[worker]["week"]
    month = workers[worker]["month"]
    return f"📊 Hisobot ({worker}):\nBugun: {day}\nHafta: {week}\nOy: {month}"

# 🚀 /start komandasi
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Salom! 👋 Hisobot botiga xush kelibsiz.\n\n"
                          "➕ Ishchi qo‘shish uchun: /add ism\n"
                          "📊 Hisobot uchun: /report ism\n"
                          "➕ yoki ➖ pul qo‘shish/ayirish uchun: /plus yoki /minus")

# ➕ Ishchi qo‘shish
@bot.message_handler(commands=['add'])
def add_worker(message):
    try:
        name = message.text.split(" ", 1)[1]
        if name not in workers:
            workers[name] = {"today": 0, "week": 0, "month": 0}
            bot.reply_to(message, f"✅ Ishchi qo‘shildi: {name}")
        else:
            bot.reply_to(message, f"⚠️ {name} allaqachon ro‘yxatda bor.")
    except:
        bot.reply_to(message, "❌ Foydalanish: /add Ism")

# ➕ Pul qo‘shish
@bot.message_handler(commands=['plus'])
def plus_money(message):
    try:
        name, amount = message.text.split(" ", 2)[1:]
        amount = int(amount)
        if name in workers:
            workers[name]["today"] += amount
            workers[name]["week"] += amount
            workers[name]["month"] += amount
            bot.reply_to(message, f"💰 {name} ga +{amount} qo‘shildi.")
        else:
            bot.reply_to(message, "❌ Bunday ishchi topilmadi.")
    except:
        bot.reply_to(message, "❌ Foydalanish: /plus Ism Miqdor")

# ➖ Pul ayirish
@bot.message_handler(commands=['minus'])
def minus_money(message):
    try:
        name, amount = message.text.split(" ", 2)[1:]
        amount = int(amount)
        if name in workers:
            workers[name]["today"] -= amount
            workers[name]["week"] -= amount
            workers[name]["month"] -= amount
            bot.reply_to(message, f"💸 {name} dan -{amount} ayirildi.")
        else:
            bot.reply_to(message, "❌ Bunday ishchi topilmadi.")
    except:
        bot.reply_to(message, "❌ Foydalanish: /minus Ism Miqdor")

# 📊 Hisobot
@bot.message_handler(commands=['report'])
def report(message):
    try:
        name = message.text.split(" ", 1)[1]
        if name in workers:
            bot.reply_to(message, get_report(name))
        else:
            bot.reply_to(message, "❌ Bunday ishchi yo‘q.")
    except:
        bot.reply_to(message, "❌ Foydalanish: /report Ism")

# 🔄 Botni doimiy ishlashda ushlab turish
bot.polling(none_stop=True)
