import os
import requests
import telebot
from telebot import apihelper

# تلاش برای تنظیم خودکار پروکسی محلی برای عبور از فیلتر تلگرام
proxy_ports = [1080, 10808, 8080, 8580, 9050, 10809]
for port in proxy_ports:
  try:
    test_res = requests.get(
        "https://api.telegram.org",
        proxies={
            "http": f"socks5://127.0.0.1:{port}",
            "https": f"socks5://127.0.0.1:{port}",
        },
        timeout=2,
    )
    if test_res.status_code < 500:
      apihelper.proxy = {
          "http": f"socks5://127.0.0.1:{port}",
          "https": f"socks5://127.0.0.1:{port}",
      }
      print(f"Connected to Telegram via local proxy on port {port}")
      break
  except:
    pass

TOKEN = "123456789:ABCdefGHIjklmNoPQRstuVWXyz"
bot = telebot.TeleBot(TOKEN)


def get_gold_price():
  try:
    url = "https://query1.finance.yahoo.com/v8/finance/chart/GC=F?interval=1m&range=1d"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers, timeout=10)
    data = response.json()
    price = data["chart"]["result"][0]["meta"]["regularMarketPrice"]
    return price
  except Exception as e:
    print(f"Error fetching gold price: {e}")
    return None


@bot.message_handler(commands=["start"])
def send_welcome(message):
  bot.reply_to(
      message,
      "سلام! ربات مدیریت ترید طلا فعال شد.\nبرای دریافت قیمت لحظه‌ای طلا دستور"
      " /price را ارسال کنید.",
  )


@bot.message_handler(commands=["price"])
def send_price(message):
  price = get_gold_price()
  if price:
    bot.reply_to(
        message,
        f"🟡 قیمت لحظه‌ای طلا (Gold Futures):\n`{price}` دلار",
        parse_mode="Markdown",
    )
  else:
    bot.reply_to(message, "خطا در دریافت قیمت طلا از سرور.")


print("Bot is running locally with smart proxy detection...")
bot.infinity_polling()
