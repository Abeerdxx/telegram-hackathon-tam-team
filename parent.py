from config import connection, TOKEN, TELEGRAM_SEND_MESSAGE_URL
import requests

def ask_question(question, chat_id):
    with connection.cursor() as cursor:
        question = "'" + question + "'"
        query = f"SELECT answer FROM QA WHERE question = {question}"
        cursor.execute(query)
        res = cursor.fetchone()
        if res is not None:
            requests.get(TELEGRAM_SEND_MESSAGE_URL.format(TOKEN, chat_id, res))
        else:
            query = f"SELECT * FROM parentsQuestions WHERE question = {question}"
            cursor.execute(query)
            res = cursor.fetchone()
            if res is None:
                query = f"INSERT INTO parentsQuestions VALUES({chat_id},{question})"
                cursor.execute(query)
            requests.get(TELEGRAM_SEND_MESSAGE_URL.format(TOKEN, chat_id, "There is no answer yet, I will check with the "
                                                                          "teacher and get back to you"))
        connection.commit()

def ask_question2(question, chat_id, class_):
    with connection.cursor() as cursor:
        question = "'" + question + "'"
        query = f"SELECT answer FROM QA WHERE question = {question}"
        cursor.execute(query)
        res = cursor.fetchone()
        if res is not None:
            res = res['answer']
            requests.get(TELEGRAM_SEND_MESSAGE_URL.format(TOKEN, chat_id, res))
        else:
            query = f"SELECT * FROM parentsQuestions WHERE question = {question}"
            cursor.execute(query)
            res = cursor.fetchone()
            if res is None:
                query = f"SELECT * FROM users WHERE job = 'main teacher' and class = {class_}"
                cursor.execute(query)
                res = cursor.fetchone()
                if res is not None:
                    requests.get(TELEGRAM_SEND_MESSAGE_URL.format(TOKEN, res['chat_id'], "You have a new question:\n" +
                                                                  question + "\nStart your answer with @ans"))
                else:
                    query = f"SELECT * FROM users WHERE job = 'teacher' and class = {class_}"
                    cursor.execute(query)
                    res = cursor.fetchone()
                    if res is not None:
                        requests.get(TELEGRAM_SEND_MESSAGE_URL.format(TOKEN, res['chat_id'], "You have a new question:\n" +
                                                                      question + "\nStart your answer with @ans"))
            requests.get(TELEGRAM_SEND_MESSAGE_URL.format(TOKEN, chat_id, "There is no answer yet, I will check with the "
                                                                          "teacher and get back to you"))
    return chat_id
