from telegram import *
from telegram.ext import *
import requests
from db import add_order
from config import *

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("💰 Buy", callback_data="buy")]]
    await update.message.reply_text(
        "🔥 Welcome to Premium Bot",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def buy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    keyboard = [
        [InlineKeyboardButton("Crypto", callback_data="crypto")],
        [InlineKeyboardButton("PayPal", callback_data="paypal")],
        [InlineKeyboardButton("Revolut", callback_data="revolut")]
    ]

    await query.message.reply_text(
        "Choose payment:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def crypto(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = str(query.from_user.id)

    url = "https://api.nowpayments.io/v1/invoice"
    headers = {"x-api-key": NOWPAYMENTS_API_KEY}

    data = {
        "price_amount": 5,
        "price_currency": "eur",
        "order_id": user_id
    }

    r = requests.post(url, json=data, headers=headers)
    invoice = r.json()

    payment_id = invoice["id"]
    pay_url = invoice["invoice_url"]

    add_order(user_id, payment_id)

    await query.message.reply_text(f"💎 Pay:\n{pay_url}")

async def paypal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.message.reply_text(
        f"PayPal:\n{PAYPAL_LINK}"
    )

async def revolut(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.message.reply_text(
        f"Revolut:\n{REVOLUT_LINK}"
    )

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(buy, pattern="buy"))
app.add_handler(CallbackQueryHandler(crypto, pattern="crypto"))
app.add_handler(CallbackQueryHandler(paypal, pattern="paypal"))
app.add_handler(CallbackQueryHandler(revolut, pattern="revolut"))

app.run_polling()