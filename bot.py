import telebot
from datetime import datetime

# Bu joyga tokeningizni qo'ying
TOKEN = "7364613353:AAFx9UCllvhgw773ER0nHn3nwDe0jrdd-bA"
bot = telebot.TeleBot(TOKEN)

# Ishchilar ma'lumotlari
workers = {}

# Yordamchi funksiya
def get_report(worker):
    day = workers[worker]["today"]
    week = workers[worker]["week"]
    month = workers[worker]["month"]
    return f"📊 Hisobot ({worker}):\nBugun: {day}\nHafta: {week}\nOy: {month}"

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Salom! 👋 Hisobot botiga xush kelibsiz.\n\nIshchilarni qo‘shish uchun /add ism yozing")

@bot.message_handler(commands=['add'])
def add_worker(message):
    try:
        name = message.text.split(" ", 1)[1]
        if name not in workers:
            workers[name] = {"today": 0, "week": 0, "month": 0}
            bot.reply_to(message, f"✅ Ishchi qo‘shildi: {name}")
        else:
            bot.reply_to(message, "⚠️ Bu ishchi allaqachon mavjud")
    except:
        bot.reply_to(message, "❌ Foydalanish: /add Nomi")

@bot.message_handler(commands=['plus'])
def plus_money(message):
    try:
        _, name, amount = message.text.split()
        amount = int(amount)
        if name in workers:
            workers[name]["today"] += amount
            workers[name]["week"] += amount
            workers[name]["month"] += amount
            bot.reply_to(message, f"💰 {name} kassasiga +{amount} qo‘shildi")
        else:
            bot.reply_to(message, "❌ Bunday ishchi topilmadi")
    except:
        bot.reply_to(message, "❌ Foydalanish: /plus ism summa")

@bot.message_handler(commands=['minus'])
def minus_money(message):
    try:
        _, name, amount = message.text.split()
        amount = int(amount)
        if name in workers:
            workers[name]["today"] -= amount
            workers[name]["week"] -= amount
            workers[name]["month"] -= amount
            bot.reply_to(message, f"💸 {name} kassasidan -{amount} olindi")
        else:
            bot.reply_to(message, "❌ Bunday ishchi topilmadi")
    except:
        bot.reply_to(message, "❌ Foydalanish: /minus ism summa")

@bot.message_handler(commands=['report'])
def report(message):
    try:
        name = message.text.split(" ", 1)[1]
        if name in workers:
            bot.reply_to(message, get_report(name))
        else:
            bot.reply_to(message, "❌ Bunday ishchi topilmadi")
    except:
        bot.reply_to(message, "❌ Foydalanish: /report ism")

print("✅ Bot ishga tushdi...")
bot.infinity_polling()
