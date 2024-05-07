import sqlite3


class Database:
    def __init__(self):
        self.connect = sqlite3.connect('102.db')
        self.cursor = self.connect.cursor()
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS speak 
                        (id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_name TEXT,
                        nickname TEXT,
                        message TEXT, 
                        tokens INTEGER,
                        blocks INTEGER,
                        gpt_tokens INTEGER)""")
        self.connect.commit()

    def check_user_exists(self, id):
        self.cursor.execute("""SELECT id FROM speak
                             WHERE id = ?""",
                            (id,))
        data = self.cursor.fetchone()
        return data is not None

    def add_user(self, id, user_name, nickname):
        self.cursor.execute("INSERT INTO speak VALUES(?,?,?,?,?,?,?);",
                            (id, user_name, nickname, '', 1000, 10, 3000))
        self.connect.commit()

    def add_message(self, id, message):
        self.cursor.execute("UPDATE speak SET message = ? WHERE id = ?", (message, id))
        self.connect.commit()

# вычитание токенов для синтеза речи пользователя
    def add_tokens(self, id, tokens):
        self.cursor.execute("UPDATE speak SET tokens = tokens - ? WHERE id = ?", (tokens, id))
        self.connect.commit()

    def update_to_zero(self, id):
        self.cursor.execute("UPDATE speak SET message = '' WHERE id = ?", (id,))
        self.connect.commit()

# проверка токенов для синтеза речи пользователя
    def get_tokens(self, id):
        self.cursor.execute("SELECT tokens FROM speak WHERE id = ?", (id,))
        result = self.cursor.fetchone()
        if result:
            return result[0]
        else:
            return None

# вычитание аудио блоков пользователя
    def minus_block(self, id, blocks_to_subtract):
        self.cursor.execute("SELECT blocks FROM speak WHERE id =?", (id,))
        current_blocks = self.cursor.fetchone()[0]
        new_blocks = current_blocks - blocks_to_subtract
        self.cursor.execute("UPDATE speak SET blocks =? WHERE id =?", (new_blocks, id))
        self.connect.commit()

# проверка аудио блоков пользователя
    def check_blocks(self, id):
        self.cursor.execute("SELECT blocks FROM speak WHERE id = ?", (id,))
        result = self.cursor.fetchone()
        if result:
            return result[0]
        else:
            return None

#    """подсчёт пользователей"""
    def get_total_users_count(self):
        self.cursor.execute("SELECT COUNT(*) FROM speak")
        total_users_count = self.cursor.fetchone()[0]
        return total_users_count

# проверка токенов гпт
    def check_gpt_tokens(self, id):
        self.cursor.execute("SELECT gpt_tokens FROM speak WHERE id = ?", (id,))
        result = self.cursor.fetchone()
        if result:
            return result[0]
        else:
            return None

# вычитание токенов гпт
    def minus_gpt_tokens(self, id, tokens_used):
        self.cursor.execute("UPDATE speak SET gpt_tokens = gpt_tokens - ? WHERE id = ?", (tokens_used, id))
        self.connect.commit()


    def close(self):
        self.connect.close()
