import asyncio
import logging
import os

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import (
    BotCommand,
    BotCommandScopeAllGroupChats,
    BotCommandScopeAllPrivateChats,
    BotCommandScopeChat,
    BotCommandScopeDefault,
)
from aiohttp import web

import config
import db
from handlers import admin, group, menu, start

GROUP_CMDS = [
    BotCommand(command="quiz", description="Testni boshlash"),
    BotCommand(command="top", description="Guruh reytingi"),
    BotCommand(command="duel", description="1 ga 1 musobaqa"),
    BotCommand(command="battle", description="Sinflar jangi"),
    BotCommand(command="stop", description="Testni to'xtatish"),
]


async def set_commands(bot: Bot) -> None:
    # Shaxsiy chatda "/" menyusi bo'sh: o'quvchilar va adminlar tugmalardan foydalanadi
    await bot.delete_my_commands(scope=BotCommandScopeDefault())
    await bot.delete_my_commands(scope=BotCommandScopeAllPrivateChats())
    # Guruhlarda quiz bot singari buyruqlar
    await bot.set_my_commands(GROUP_CMDS, scope=BotCommandScopeAllGroupChats())
    # Eski admin buyruqlari menyusini tozalash
    for admin_id in config.ADMIN_IDS:
        try:
            await bot.delete_my_commands(scope=BotCommandScopeChat(chat_id=admin_id))
        except Exception as e:  # admin botga hali /start bosmagan bo'lishi mumkin
            logging.warning("Admin %s menyusi tozalanmadi: %s", admin_id, e)


async def start_health_server():
    """Render 'Web Service' uchun oddiy sog'liq tekshiruvi (PORT bo'lsa ishga tushadi)."""
    port = int(os.getenv("PORT", "0"))
    if not port:
        return None
    app = web.Application()

    async def ok(_request):
        return web.Response(text="ok")

    app.router.add_get("/", ok)
    runner = web.AppRunner(app)
    await runner.setup()
    await web.TCPSite(runner, "0.0.0.0", port).start()
    return runner


async def main() -> None:
    logging.basicConfig(level=logging.INFO)
    if not config.BOT_TOKEN or not config.DATABASE_URL:
        raise SystemExit("BOT_TOKEN va DATABASE_URL .env faylida bo'lishi kerak.")

    await db.init_db(config.DATABASE_URL)

    bot = Bot(config.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(admin.router)
    dp.include_router(group.router)
    dp.include_router(menu.router)
    dp.include_router(start.router)

    await set_commands(bot)
    await start_health_server()
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
