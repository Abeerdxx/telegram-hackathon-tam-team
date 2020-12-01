TOKEN = '1434503036:AAGfw6YnF5qK2m77D9YprlPvstfC_yomZso'
NKROG_URL = "https://e3bfd58c3815.ngrok.io"
TELEGRAM_INIT_WEBHOOK_URL = 'https://api.telegram.org/bot{}/setWebhook?url={}/message'.format(TOKEN, NKROG_URL)
TELEGRAM_SEND_MESSAGE_URL = "https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}"
