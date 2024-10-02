import asyncio
from aiogram import Bot, Dispatcher
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database

from handlers import users
from config_data import Config, load_config
from db.models import Base


async def main():
    config: Config = load_config()

    bot = Bot(token=config.tg_bot.token)
    dp = Dispatcher()

    dp.include_router(users.router)
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

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())