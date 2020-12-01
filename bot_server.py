from flask import Flask, request, Response
from config import TELEGRAM_INIT_WEBHOOK_URL
from botAPI import start
import requests

app = Flask(__name__)

requests.get(TELEGRAM_INIT_WEBHOOK_URL)


@app.route('/message', methods=["POST"])
def handle_message():
    req = request.get_json()
    chat_id = request.get_json()['message']['chat']['id']
    start(chat_id)
    print("got it")
    return Response("success")


if __name__ == "__main__":
    app.run(port=3002)
