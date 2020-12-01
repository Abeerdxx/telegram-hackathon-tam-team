from config import connection


def ask_question(question, chat_id):
    answer = None
    with connection.cursor() as cursor:
        query = f"SELECT answer FROM QA WHERE question = {question}"
        cursor.execute(query)
        res = cursor.fetchone()
        if res is not None:
            answer = res
        else:
            query = f"INSERT INTO parentsQuestions VALUES({chat_id},{question})"
            cursor.execute(query)
        connection.commit()
    return answer
