import asyncio
import os

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

from applications.services.submit_task import SubmitTask
from domain.state import TaskRequest

load_dotenv()

submit_task = SubmitTask()


async def start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    if update.message:
        await update.message.reply_text("Factorie-Ia conectada.\nEnvíame una tarea.")


async def handle_message(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    if not update.message or not update.message.text:
        return

    request = TaskRequest(
        description=update.message.text,
        source="telegram",
    )

    try:
        result = await asyncio.to_thread(
            submit_task.submit,
            request,
        )
        await update.message.reply_text(result.response)
    except Exception:
        await update.message.reply_text("No pude procesar la tarea. Revisa los logs.")
        raise


def run_telegram_bot() -> None:
    token = os.getenv("TELEGRAM_BOT_TOKEN")

    if not token:
        raise RuntimeError("Falta TELEGRAM_BOT_TOKEN en el archivo .env")

    app = Application.builder().token(token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            handle_message,
        )
    )

    print("Factorie-Ia escuchando mensajes de Telegram...")
    app.run_polling()


if __name__ == "__main__":
    run_telegram_bot()
