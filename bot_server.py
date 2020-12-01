from flask import Flask, request, Response
from config import TELEGRAM_INIT_WEBHOOK_URL
from my_bot import MyBot

app = Flask(__name__)

MyBot.init_webhook(TELEGRAM_INIT_WEBHOOK_URL)


@app.route('/message', methods=["POST"])
def handle_message():
    req = request.get_json()
    bot = MyBot()
    bot.parse_request(req)
    success = bot.action()
    return Response(success)


if __name__ == "__main__":
    app.run(port=3002)
