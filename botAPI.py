from config import connection
role = None


def start(chat_id):
    global role
    with connection.cursor() as cursor:
        sql = "SELECT * FROM `users` where `chat_id`=%s"
        cursor.execute(sql, chat_id)
        result = cursor.fetchone()
        if result is not None:
            role = result['role']
        else:
            role = input("Are you a parent or a teacher?")
            class_ = input("What is your class' number?")
            sql = "INSERT INTO `Users` VALUES (%s,%s,%s)"
            cursor.execute(sql, (role, class_, chat_id))
    connection.commit()

