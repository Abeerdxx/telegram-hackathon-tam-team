import requests
from config import connection, TOKEN, TELEGRAM_SEND_MESSAGE_URL
from parent import ask_question
from teacher import *


def what_can_i_do(chat_id, role):
    if role == "teacher":
        requests.get(
            TELEGRAM_SEND_MESSAGE_URL.format(TOKEN, chat_id, "You can do one of the following things:\n"
                                                             "/answer_question <answer> to add answer , where you can answer a "
                                                             "question that does not have an answer in the "
                                                             "FAQ\n "
                                                             "/add_announcement <announcement> to send, where you can send an "
                                                             "announcement to every parent in the class you "
                                                             "are in\n"
                                                             "/add_question <Question> to add"))
    else:
        requests.get(
            TELEGRAM_SEND_MESSAGE_URL.format(TOKEN, chat_id, "/ask_question <Question> to ask, where you can ask"
                                                             " question and get answer right away!! "))


def parse_command(com, chat_id):
    class_ = None
    role = None
    parsed = com.split(" ", 1)  # maxsplit = 1
    first_command = parsed[0]
    with connection.cursor() as cursor:
        sql = "SELECT * FROM `users` where `chat_id`=%s"
        cursor.execute(sql, chat_id)
        result = cursor.fetchone()
        if result is not None:
            role = result['role']
            class_ = result['class']
    if first_command == "/start":
        start(chat_id)
    elif first_command == "teacher" or first_command == "parent":
        role = first_command
        requests.get(TELEGRAM_SEND_MESSAGE_URL.format(TOKEN, chat_id, "What class are you in?"))
    elif first_command == "class":
        class_ = parsed[1]
        add_user(chat_id, role, class_)
        requests.get(
            TELEGRAM_SEND_MESSAGE_URL.format(TOKEN, chat_id, "Welcome!! you have been registered as"
                                                             " " + role + f" with class {class_}"))
    elif first_command == "/answer":
        if role == "parent":
            requests.get(TELEGRAM_SEND_MESSAGE_URL.format(TOKEN, chat_id, "you are a parent"))
        else:
            answer_the_last_question(parsed[1], chat_id)
    elif first_command == "/ask_question":
        if len(parsed) <= 1:
            requests.get(TELEGRAM_SEND_MESSAGE_URL.format(TOKEN, chat_id, "improper format"))
        else:
            ask_question(parsed[1], chat_id)
    elif first_command == "/answer_question":
        if role == "parent":
            requests.get(TELEGRAM_SEND_MESSAGE_URL.format(TOKEN, chat_id, "you are a parent"))
        else:
            answer_question(chat_id)
    elif first_command == "/add_question":
        if role == "parent":
            requests.get(TELEGRAM_SEND_MESSAGE_URL.format(TOKEN, chat_id, "you are a parent"))
        else:
            if len(parsed) <= 1:
                requests.get(TELEGRAM_SEND_MESSAGE_URL.format(TOKEN, chat_id, "improper format"))
            else:
                add_question(parsed[1], chat_id)
    elif first_command == "@answer":
        if role == "parent":
            requests.get(TELEGRAM_SEND_MESSAGE_URL.format(TOKEN, chat_id, "you are a parent"))
        else:
            if len(parsed) <= 1:
                requests.get(TELEGRAM_SEND_MESSAGE_URL.format(TOKEN, chat_id, "improper format"))
            else:
                answer_add_question(parsed[1], chat_id)
    elif first_command == "/add_announcement":
        if role == "parent":
            requests.get(TELEGRAM_SEND_MESSAGE_URL.format(TOKEN, chat_id, "you are a parent"))
        else:
            if len(parsed) <= 1:
                requests.get(TELEGRAM_SEND_MESSAGE_URL.format(TOKEN, chat_id, "improper format"))
            else:
                add_announcement(parsed[1], class_)
    else:
        requests.get(TELEGRAM_SEND_MESSAGE_URL.format(TOKEN, chat_id, "unavailable command"))
    return ""


def add_user(chat_id, role, class_):
    with connection.cursor() as cursor:
        sql = "INSERT INTO `Users` VALUES (%s,%s,%s)"
        cursor.execute(sql, (role, class_, chat_id))
    connection.commit()


def start(chat_id):
    with connection.cursor() as cursor:
        sql = "SELECT * FROM `users` where `chat_id`=%s"
        cursor.execute(sql, chat_id)
        result = cursor.fetchone()
        if result is not None:
            role = result['role']
            requests.get(TELEGRAM_SEND_MESSAGE_URL.format(TOKEN, chat_id, "Hi, what would you like to do today?"))
        else:
            requests.get(TELEGRAM_SEND_MESSAGE_URL.format(TOKEN, chat_id, "Are you a parent or a teacher?"))
