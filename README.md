# MyBarberbot# Telegram Bot Deployment

## Heroku'ga joylash uchun qadamlar:

1. Heroku hisobi yarating
2. Yangi app yarating
3. GitHub reponi ulang yoki CLI orqali kodni yuklang
4. Config Vars qo'shing:

```
BOT_TOKEN: your_telegram_bot_token
WEB_APP_URL: https://your-web-app.com
ADMIN_ID: 123456789 (optional)
USE_WEBHOOK: false (yoki true)
WEBHOOK_URL: https://your-app-name.herokuapp.com/webhook (agar USE_WEBHOOK=true bo'lsa)
```

5. Resources menyusida `web` va `worker` processlarni yoqing

## Mahalliy ishga tushirish

```bash
pip install -r requirements.txt
python bot.py
```