import datetime
import logging
from asyncio import sleep

import psycopg2

logger = logging.getLogger(__name__)


class Repository:
    def __init__(self, config):
        self.__dbname = config["postgres"]["dbname"]
        self.__user = config["postgres"]["user"]
        self.__password = config["postgres"]["password"]
        self.__host = config["postgres"]["host"]
        self.__connection = None

    async def connect(self):
        for i in range(3):
            logger.info(f"Trying to connect to Postgres. Attempt {i + 1}")
            try:
                self.__connection = psycopg2.connect(
                    dbname=self.__dbname,
                    user=self.__user,
                    password=self.__password,
                    host=self.__host
                )
                logger.info("Connected to Postgres")
                break
            except:
                logger.error("Cannot connect to Postgres")
                await sleep(5)
        else:
            raise ConnectionError("Can not connect to db after 3 attempts")

    def is_user_registered(self, userid) -> bool:
        cursor = self.__connection.cursor()
        cursor.execute("SELECT * FROM users WHERE userid = %s", (userid,))
        user = cursor.fetchone()
        logger.info(f"Fetching user with id {userid}")
        return user is not None

    def is_trial_used(self, userid) -> bool:
        cursor = self.__connection.cursor()
        cursor.execute("SELECT * FROM users WHERE userid = %s", (userid,))
        user = cursor.fetchone()
        logger.info(f"Fetching user with id {userid}")
        if user is None:
            logger.warning(f"User with id {userid} doesnot exist")
            return False
        else:
            return user[1]

    def insert_user(self, user):
        cursor = self.__connection.cursor()
        cursor.execute(
            "INSERT INTO users (userid, trial, valid_until) "
            "VALUES (%s, %s, %s)",
            (user.userid, False, None)
        )
        self.__connection.commit()
        logger.info(f"Registered new user with id {user.userid}.")

    def activate_trial(self, userid) -> datetime.datetime:
        expiration = datetime.datetime.utcnow()
        expiration += datetime.timedelta(days=7)
        cursor = self.__connection.cursor()
        cursor.execute(
            "UPDATE users "
            "SET trial = TRUE, valid_until = %s "
            "WHERE userid = %s",
            (expiration, userid)
        )
        self.__connection.commit()
        logger.info(f"Activated trial for user with id {userid}. Expires on {expiration}.")
        return expiration

    def activate_subscription(self, userid, days) -> datetime.datetime:
        expiration = datetime.datetime.utcnow()
        expiration += datetime.timedelta(days=days)
        cursor = self.__connection.cursor()
        cursor.execute(
            "UPDATE users "
            "SET valid_until = %s"
            "WHERE userid = %s",
            (expiration, userid)
        )
        self.__connection.commit()
        logger.info(f"Activated subscription for user with id {userid}. Expires on {expiration}.")
        return expiration

    def get_expiration(self, userid) -> datetime.datetime:
        cursor = self.__connection.cursor()
        cursor.execute(
            "SELECT valid_until "
            "FROM users "
            "WHERE userid = %s",
            (userid,)
        )
        logger.info(f"Fetching expiration for user with id {userid}")
        return cursor.fetchone()[0]

    def insert_many_articles(self, articles: list):
        cursor = self.__connection.cursor()
        new_articles = []
        for article in articles:
            cursor.execute(
                "INSERT INTO articles (articleid) VALUES (%s) ON CONFLICT DO NOTHING",
                (article.article_id,)
            )
            if cursor.rowcount > 0:
                new_articles.append(article)
                logger.info(f"Inserted article with id {article.article_id}")

        self.__connection.commit()
        return new_articles

    def get_userids_to_notify(self):
        cursor = self.__connection.cursor()
        cursor.execute(
            "SELECT userid "
            "FROM users "
            "WHERE valid_until > %s",
            (datetime.datetime.utcnow(),)
        )
        logger.info("Fetching users to notify.")
        userids = cursor.fetchall()
        return userids


class User:
    def __init__(self, userid):
        self.userid = userid
