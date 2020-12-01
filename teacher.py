from config import connection, TELEGRAM_SEND_MESSAGE_URL, TOKEN
import requests
the_question_to_answer = ""


def answer_question(teacher_chat_id):
    with connection.cursor() as cursor:
        quary = "SELECT * FROM parentsQuestions LIMIT 1"
        cursor.execute(quary)
        result = cursor.fetchone()
        if result is not None:
            requests.get(TELEGRAM_SEND_MESSAGE_URL.format(TOKEN, teacher_chat_id, result['question']) +
                         "\n write #answer to answer the question")
            quary2 = f"INSERT INTO parentsQuestionsQueue VALUES({result['chat_id']},{result['question']})"
            cursor.execute(quary2)
            quary3 = f"DELETE FROM parentsQuestions WHERE question = {result['question']}"
            cursor.execute(quary3)
            connection.commit()

        else:
            requests.get(TELEGRAM_SEND_MESSAGE_URL.format(TOKEN, teacher_chat_id, "There are no questions to answer! "
                                                                                  "Thank you and have a nice day! :) "))


def answer_the_last_question(answer, teacher_chat_id):
    with connection.cursor() as cursor:
        quary = "SELECT * FROM parentsQuestionsQueue LIMIT 1"
        cursor.execute(quary)
        result = cursor.fetchone()
        if result is not None:
            requests.get(TELEGRAM_SEND_MESSAGE_URL.format(TOKEN, result['chat_id'], "The answer for your last question is :\n"
            + answer))
            quary2 = f"INSERT INTO QA VALUES({answer}, {result['question']}, {result['question']})"
            cursor.execute(quary2)
            quary3 = f"DELETE FROM parentsQuestionsQueue WHERE question = {result['question']}"
            cursor.execute(quary3)
            connection.commit()
        else:
            requests.get(TELEGRAM_SEND_MESSAGE_URL.format(TOKEN, teacher_chat_id, "THERE IS NO QUESTION TO ANSWER!!"))


def add_question(question, teacher_chat_id):
    global the_question_to_answer
    the_question_to_answer = question
    requests.get(TELEGRAM_SEND_MESSAGE_URL.format(TOKEN, teacher_chat_id, "write @answer to answer the question you added!"))


def answer_add_question(answer):
    global the_question_to_answer
    with connection.cursor() as cursor:
        quary = f"INSERT INTO QA VALUES({answer}, {the_question_to_answer}, {the_question_to_answer})"
        cursor.execute(quary)
        connection.commit()
    the_question_to_answer = ''


def add_announcement(announcement):
    with connection.cursor() as cursor:
        quary = "SELECT chat_id FROM users WHERE role = parent"
        cursor.execute(quary)
        result = cursor.fetchall()
        if result:
            for parent_chat_id in result:
                requests.get(TELEGRAM_SEND_MESSAGE_URL.format(TOKEN, parent_chat_id, announcement))