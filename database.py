import sqlite3
from pandas import DataFrame
class Database:


    def __init__(self, db_file):
        #Подключаемся к файлу БД
        self.conn = sqlite3.connect(db_file,check_same_thread=False)
        self.cursor = self.conn.cursor()

    def user_exists(self, user_id):
        #Проверяем, есть ли юзер в базе
        result = self.cursor.execute("SELECT id FROM users WHERE user_chat_id = ?", (user_id,))
        return bool(len(result.fetchall()))

    def get_user_id(self, user_id):
        #Достаем id юзера в базе по его user_id
        result = self.cursor.execute("SELECT `id` FROM `users` WHERE `user_chat_id` = ?", (user_id,))
        return result.fetchone()[0]

    def get_student_paru(self, inputdata):
        result = self.cursor.execute("SELECT Vremya, Para, Prepodavatel FROM univerparu WHERE Data = ?", (inputdata,))
        return result.fetchall()


    def get_predmet(self, predmet):
        result = self.cursor.execute("SELECT Prepodavatel FROM univerparu WHERE Para = ?",(predmet,))
        return result.fetchone()

    def add_user(self, user_id, userchatid):
        #Добавляем юзера в базу
        self.cursor.execute("UPDATE users SET user_chat_id = ? WHERE id = ?;", (userchatid,user_id))
        return self.conn.commit()
        return result.fetchall()

    def add_raspisanie(self, df):
        for row in df.itertuples():
            result = self.cursor.execute("SELECT Data, Vremya FROM univerparu WHERE Data = ? AND Vremya = ?",
                                         (row.Data, row.Vremya))
            sql_df = DataFrame(result.fetchall())
            df.drop(df.columns[[0]], axis=1)
            if sql_df.empty:
                self.cursor.execute("INSERT INTO univerparu (Day, Data, Vremya, Para, Prepodavatel) VALUES "
                                    "(?, ?, ?, ?, ?)", (row.Day, row.Data, row.Vremya, row.Para, row.Prepodavatel))
                self.conn.commit()
            else:
                self.cursor.execute("UPDATE univerparu SET Day = ?, Data = ?, Vremya = ?, Para = ?, Prepodavatel "
                                    "= ? WHERE Data = ? AND Vremya = ?", (row.Day, row.Data, row.Vremya,
                                                    row.Para, row.Prepodavatel, row.Data, row.Vremya))
                self.conn.commit()
        return self.conn.commit()

    def close(self):
        #Закрываем соединение с БД
        self.connection.close()

