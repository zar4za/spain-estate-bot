import datetime
from asyncio import sleep

import psycopg2


class Repository:
    def __init__(self, config):
        self.__dbname = config["postgres"]["dbname"]
        self.__user = config["postgres"]["user"]
        self.__password = config["postgres"]["password"]
        self.__host = config["postgres"]["host"]
        self.__connection = None

    async def connect(self):
        for i in range(3):
            print(f"Trying to connect to Postgres. Attempt {i + 1}")
            try:
                self.__connection = psycopg2.connect(
                    dbname=self.__dbname,
                    user=self.__user,
                    password=self.__password,
                    host=self.__host
                )
                print("Connected to Postgres")
                break
            except:
                print("Cannot connect to Postgres")
                await sleep(5)
        else:
            raise ConnectionError("Can not connect to db after 3 attempts")

    def is_user_registered(self, userid) -> bool:
        cursor = self.__connection.cursor()
        cursor.execute("SELECT * FROM users WHERE userid = %s", (userid,))
        user = cursor.fetchone()
        return user is not None

    def is_trial_used(self, userid) -> bool:
        cursor = self.__connection.cursor()
        cursor.execute("SELECT * FROM users WHERE userid = %s", (userid,))
        user = cursor.fetchone()

        if user is None:
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
        print(f"DB: Registered new user with id {user.userid}.")

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
        print(f"DB: Activated trial for user with id {userid}. Expires on {expiration}.")
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
        print(f"DB: Activated subscription for user with id {userid}. Expires on {expiration}.")
        return expiration

    def insert_many_articles(self, articles: list):
        cursor = self.__connection.cursor()
        cursor.execute()
        self.__connection.commit()


class User:
    def __init__(self, userid):
        self.userid = userid
