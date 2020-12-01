import requests
from config import connection, TOKEN, TELEGRAM_SEND_MESSAGE_URL

role = None
class_ = None


def parse_command(com, chat_id):
    global role, class_
    parsed = com.split()
    first_command = parsed[0]
    if first_command == "/start":
        start(chat_id)
    elif first_command == "teacher" or first_command == "parent":
        role = first_command
        requests.get(TELEGRAM_SEND_MESSAGE_URL.format(TOKEN, chat_id, "What class are you in?"))
    elif first_command == "class":
        class_ = parsed[1]
        add_user(chat_id)
    elif first_command == "#answer":
        if role == "parent":
            requests.get(TELEGRAM_SEND_MESSAGE_URL.format(TOKEN, chat_id, "you are a parent"))
    return ""


def add_user(chat_id):
    with connection.cursor() as cursor:
        sql = "INSERT INTO `Users` VALUES (%s,%s,%s)"
        cursor.execute(sql, (role, class_, chat_id))
    connection.commit()


def start(chat_id):
    global role
    with connection.cursor() as cursor:
        sql = "SELECT * FROM `users` where `chat_id`=%s"
        cursor.execute(sql, chat_id)
        result = cursor.fetchone()
        if result is not None:
            role = result['role']
        else:
            requests.get(TELEGRAM_SEND_MESSAGE_URL.format(TOKEN, chat_id, "Are you a parent or a teacher?"))
