import datetime

import telegram
from telegram import constants, Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import CommandHandler, ContextTypes, Application, MessageHandler, filters


class TgBot:
    def __init__(self, config):
        token = config["telegram"]["token"]
        whitelist = config["telegram"]["whitelist"]

        self.use_whitelist = False
        self.app = Application.builder().token(token).build()

        message = "OFF"

        if any(whitelist):
            self.use_whitelist = True
            self.whitelist = whitelist
            message = "ON"

        print("Whitelist mode is " + message)

    async def start(self):
        print("Registering command handlers")
        self.app.add_handler(CommandHandler("start", self.greet))
        self.app.add_handler(MessageHandler(filters.Regex("Подписка"), self.on_subscription))
        print("Starting Telegram bot")
        await self.app.initialize()
        await self.app.start()
        await self.app.updater.start_polling()
        print("Telegram bot started")

    async def stop(self):
        print("Shutting down Telegram bot")
        await self.app.updater.stop()
        await self.app.stop()
        await self.app.shutdown()
        print("Telegram bot shut down")

    async def greet(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        buttons = [[
            "Подписка",
            "Личный кабинет",
            "Помощь"
        ]]

        reply_markup = ReplyKeyboardMarkup(buttons)

        await context.bot.send_message(
            chat_id=update.effective_user.id,
            text=(
                f"Добро пожаловать в <b>{self.app.bot.first_name}</b>.\n"
                f"\n"
                f"Этот бот отправляет уведомления о новых объявлениях c сайта "
                f"<a href=\"https://idealista.com\">idealista.com</a>.  На данный момент отправляются уведомления "
                f"только о квартирах из Валенсии стомостью менее 100 тысяч евро. В будущем планируются "
                f"пользовательские фильтры для объявлений и другие сайты с недвижимостью.\n"
                f"\n"
                f"Для использования бота необходима подписка. В первый раз можно взять бесплатно пробную "
                f"подписку на 7 дней."
            ),
            parse_mode=constants.ParseMode.HTML,
            disable_web_page_preview=True,
            reply_markup=reply_markup
        )

    async def on_subscription(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        used_trial = False
        valid_until = datetime.datetime.utcnow()
        buttons = ['Главная']

        if not used_trial:
            buttons.append('Пробная подписка')
        if valid_until < datetime.datetime.utcnow():
            buttons.append('Купить подписку на месяц')
        else:
            buttons.append('Приостановить подписку')

        reply_markup = ReplyKeyboardMarkup([buttons])

        await context.bot.send_message(
            chat_id=update.effective_user.id,
            text=(
                f"Ваша подписка действительна до: {valid_until}\n"
            ),
            parse_mode=constants.ParseMode.HTML,
            disable_web_page_preview=True,
            reply_markup=reply_markup
        )
