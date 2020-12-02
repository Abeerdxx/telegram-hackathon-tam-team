import requests
from config import connection, TOKEN, TELEGRAM_SEND_MESSAGE_URL
from parent import ask_question, asker_id, ask_question2
from teacher import *

role_ = ""


def what_can_i_do(chat_id, role):
    if role == "teacher":
        requests.get(
            TELEGRAM_SEND_MESSAGE_URL.format(TOKEN, chat_id,
                                             "You are the boss 😎 you can do one of the following things:\n"
                                             "/answer_question <Answer> to add answer , where you can answer a "
                                             "question that does not have an answer in the "
                                             "FAQ\n "
                                             "/add_announcement <Announcement> to send, where you can send an "
                                             "announcement to every parent in the class you "
                                             "are in\n"
                                             "/add_question <Question> to add general question"))
    else:
        requests.get(
            TELEGRAM_SEND_MESSAGE_URL.format(TOKEN, chat_id, "You can do one of the following things:\n"
                                                             "/ask_question <Question> to ask, where you can ask"
                                                             " question and get answer right away!!"))


def parse_command(com, chat_id, name):
    global role_
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
        else:
            role = role_
    if first_command == "/start":
        start(chat_id)
    elif first_command == "@ans":
        if len(parsed) <= 1:
            requests.get(TELEGRAM_SEND_MESSAGE_URL.format(TOKEN, chat_id, "You should write @ans "
                                                                          "and after it your answer"))
        else:
            return_answer_to_parent(asker_id, parsed[1])
    elif first_command.lower() == "teacher" or first_command.lower() == "parent":
        role_ = first_command
        requests.get(TELEGRAM_SEND_MESSAGE_URL.format(TOKEN, chat_id, "What class are you in?\n write class <number>\n"
                                                                      "so I can know to which class I should add you 😉"))
    elif first_command.lower() == "class":
        class_ = parsed[1]
        add_user(chat_id, role_, class_)
        requests.get(
            TELEGRAM_SEND_MESSAGE_URL.format(TOKEN, chat_id, "Welcome!! " + name + " you have been registered as"
                                                                                   " " + role_ + " In class " + class_))

        what_can_i_do(chat_id, role_)
    elif first_command == "/answer":
        if role == "parent":
            requests.get(
                TELEGRAM_SEND_MESSAGE_URL.format(TOKEN, chat_id, "You are a parent you can not answer a question 😉"))
        else:
            if len(parsed) <= 1:
                requests.get(TELEGRAM_SEND_MESSAGE_URL.format(TOKEN, chat_id, "You should write /answer "
                                                                              "and after it your answer"))
            else:
                answer_the_last_question(parsed[1], chat_id)
    elif first_command == "/ask_question":
        if len(parsed) <= 1:
            requests.get(TELEGRAM_SEND_MESSAGE_URL.format(TOKEN, chat_id, "You should write /ask_question "
                                                                          "and after it your question"))
        else:
            ask_question2(parsed[1], chat_id, class_)
    elif first_command == "/answer_question":
        if role == "parent":
            requests.get(
                TELEGRAM_SEND_MESSAGE_URL.format(TOKEN, chat_id, "You are a parent you can not answer a question 😉"))
        else:
            answer_question(chat_id)
    elif first_command == "/add_question":
        if role == "parent":
            requests.get(
                TELEGRAM_SEND_MESSAGE_URL.format(TOKEN, chat_id, "You are a parent you can not add a question 😔"))
        else:
            if len(parsed) <= 1:
                requests.get(TELEGRAM_SEND_MESSAGE_URL.format(TOKEN, chat_id, "You should write /add_question "
                                                                              "and after it your question"))
            else:
                add_question(parsed[1], chat_id)
    elif first_command == "@answer":
        if role == "parent":
            requests.get(
                TELEGRAM_SEND_MESSAGE_URL.format(TOKEN, chat_id, "You are a parent you can not answer a question 😉"))
        else:
            if len(parsed) <= 1:
                requests.get(TELEGRAM_SEND_MESSAGE_URL.format(TOKEN, chat_id, "You should write @answer "
                                                                              "and after it your answer"))
            else:
                answer_add_question(parsed[1], chat_id)
    elif first_command == "/add_announcement":
        if role == "parent":
            requests.get(
                TELEGRAM_SEND_MESSAGE_URL.format(TOKEN, chat_id, "You are a parent you can not send announcement 🙃"))
        else:
            if len(parsed) <= 1:
                requests.get(TELEGRAM_SEND_MESSAGE_URL.format(TOKEN, chat_id, "You should write /add_announcement "
                                                                              "and after it your announcement"))
            else:
                add_announcement(parsed[1], class_)
    elif first_command.lower() == "hello" or first_command.lower() == "hey" or first_command.lower() == "hi" or first_command.lower() == "sup":
        requests.get(TELEGRAM_SEND_MESSAGE_URL.format(TOKEN, chat_id, f"Hey!! {name},\n"
                                                                      "My name is Tam how can I help you? \n"
                                                                      "for your role you can do the following:\n "))
        what_can_i_do(chat_id, role)
    else:
        requests.get(
            TELEGRAM_SEND_MESSAGE_URL.format(TOKEN, chat_id, "Unavailable command you can do the following:\n"))
        what_can_i_do(chat_id, role)
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
            requests.get(TELEGRAM_SEND_MESSAGE_URL.format(TOKEN, chat_id, "Hi, what would you like to do today?\n"
                                                                          "it seems you are already registered.\n"
                                                                          "Talk to technical support if you want to change register\n"
                                                                          "Basil sgier : 0533013218"))
        else:
            requests.get(TELEGRAM_SEND_MESSAGE_URL.format(TOKEN, chat_id, "Are you a parent or a teacher?"))
