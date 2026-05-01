from flask import Flask, request
from db import confirm_order, get_user
from telegram import Bot
from config import TOKEN

app = Flask(__name__)
bot = Bot(token=TOKEN)

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json

    if data["payment_status"] == "finished":
        payment_id = data["payment_id"]

        confirm_order(payment_id)
        user = get_user(payment_id)

        if user:
            user_id = user[0]

            bot.send_message(
                chat_id=user_id,
                text="✅ Payment confirmed!\n\n🎧 Your access:\nlogin: xxx\npass: xxx"
            )

    return "OK"

if __name__ == "__main__":
    app.run(port=5000)