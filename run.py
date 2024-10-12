import asyncio
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database

from handlers import users
from config_data import Config, load_config
from db.models import Base, UserManager
from keyboards import set_main_menu
from middlewares import DatabaseMiddleware


async def main():
    config: Config = load_config()

    bot = Bot(token=config.tg_bot.token,
              default=DefaultBotProperties(parse_mode=ParseMode.HTML)
              )
    dp = Dispatcher()

    await set_main_menu(bot)

    dp.include_router(users.router)
    dp.update.middleware(DatabaseMiddleware())
    # there's a URL of your database. as default, you can use "sqlite:///project.db"
    # also you can put your url using arguments of a db object like in an example below
    # db = config.db
    # DB_URL = f"{db.database}://{db.db_user}:{db.db_password}@{db.db_host}:{db.db_port}/{db.db_name}"
    DB_URL = "sqlite:///project.db"
    engine = create_engine(DB_URL)
    Session = sessionmaker(engine)
    session = Session()
    # create database only at the first time
    if not database_exists(DB_URL):
        create_database(DB_URL)
    Base.metadata.create_all(engine)

    # update workflow_data to have access to these variables in middlewares
    dp.workflow_data.update({
        'DB_URL': DB_URL,
        'usermanager': UserManager(db_engine=engine, db_session=session),
    })

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
