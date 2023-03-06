from telegram import Update
from telegram.ext import CommandHandler, ContextTypes, Application


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
        self.app.add_handler(CommandHandler("start", greet))
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


async def greet(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_user.id,
        text=(
            "Приветствую в этом чудесном боте!"
        )
    )
