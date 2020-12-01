import pymysql

TOKEN = '1430899555:AAEdXpg02t63XZRhXMqCjwtsB5UjuC7kqM8'
NKROG_URL = "https://51d781a65051.ngrok.io"
TELEGRAM_INIT_WEBHOOK_URL = 'https://api.telegram.org/bot{}/setWebhook?url={}/message'.format(TOKEN, NKROG_URL)
TELEGRAM_SEND_MESSAGE_URL = "https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}"


connection = pymysql.connect(
    host="localhost",
    user="root",
    password="password",
    db="maindb",
    charset="utf8",
    cursorclass=pymysql.cursors.DictCursor
)
