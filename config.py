TOKEN = '1414408844:AAH5uhncS96xJUs5lSijM7EStyvdYW6TWVI'
NKROG_URL = "https://615d17d0f73b.ngrok.io"
TELEGRAM_INIT_WEBHOOK_URL = 'https://api.telegram.org/bot{}/setWebhook?url={}/message'.format(TOKEN, NKROG_URL)
TELEGRAM_SEND_MESSAGE_URL = "https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}"
