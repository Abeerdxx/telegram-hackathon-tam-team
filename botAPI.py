import requests
from config import connection, TOKEN, TELEGRAM_SEND_MESSAGE_URL
from parent import ask_question
role = None
class_ = None


def parse_command(com, chat_id):
    global role, class_
    parsed = com.split(" ", 1) #maxsplit = 1
    first_command = parsed[0]
    if first_command == "/start":
        requests.get(TELEGRAM_SEND_MESSAGE_URL.format(TOKEN, chat_id, "Hi, what would you like to do today?"))
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
    elif first_command == "/ask_question":
        if len(parsed) <= 1:
            requests.get(TELEGRAM_SEND_MESSAGE_URL.format(TOKEN, chat_id, "improper format"))
        else:
            parsed[1] = parsed[1].replace('?', "")
            ask_question(parsed[1], chat_id)
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
