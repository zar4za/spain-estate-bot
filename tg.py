from telegram import Update
from telegram.ext import Updater, CommandHandler, ContextTypes, Application


class TgBot:
    def __init__(self, token, id_whitelist: list):
        self.whitelist = id_whitelist
        self.app = Application.builder().token(token).build()

        self.app.add_handler(CommandHandler('start', self.start))

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if update.effective_user.id not in self.whitelist:
            return

        await context.bot.send_message(chat_id=update.effective_user.id, text='Бот запущен.')

    def run(self):
        self.app.run_polling()

    async def send_article(self, article):
        text = article['title'] + article['specs'] + article['desc'] + 'idealista.com' + article['url']

        for userid in self.whitelist:
            try:
                print('Отправляю пользователю' + str(userid))
                await self.app.bot.send_message(chat_id=userid, text=text)
            except:
                print('Ошибка отправки пользователю' + str(userid))
