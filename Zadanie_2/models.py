from clcrypto import password_hash


class User:

    def __init__(self):
        self.__id = -1
        self.username = ""
        self.email = ""
        self.__hashed_password = ""

    def is_synchronized(self):
        return self.__id != -1

    @property
    def id(self):
        return self.__id

    @property
    def hashed_password(self):
        return self.__hashed_password

    @property
    def password(self):
        raise Exception("Cannot access plain text password")

    @password.setter
    def password(self, plain_password):
        self.__hashed_password = password_hash(plain_password)

    def __str__(self):
        return f"User(id={self.id}, name={self.username}, email={self.email})"

    def save_to_db(self, cursor):
        if self.is_synchronized():
            # update record
            sql = """UPDATE users SET username=%s, email=%s, hashed_password=%s
                WHERE id=%s"""
            try:
                values = (self.username, self.email, self.hashed_password, self.id)
                cursor.execute(sql, values)
                return True
            except Exception as e:
                print(f"Failed to update user {self}, due to {e}")
                return False
        else:
            # saving new instance using prepared statements
            sql = """INSERT INTO users(username, email, hashed_password)
                    VALUES(%s, %s, %s) RETURNING id"""
            values = (self.username, self.email, self.hashed_password)
            try:
                cursor.execute(sql, values)
                self.__id = cursor.fetchone()[0]  # albo cursor.fetchone()['id']
                return True
            except Exception as e:
                print(f"Failed to create user {self}, due to {e}")
                return False

    def delete(self, cursor):
        sql = "DELETE FROM Users WHERE id=%s"
        try:
            cursor.execute(sql, (self.__id,))
            self.__id = -1
            return True
        except Exception as e:
            print(f"Failed to delete user {self}, due to {e}")
            return False

    @staticmethod
    def load_user_by_id(cursor, user_id):
        sql = "SELECT id, username, email, hashed_password FROM users WHERE id=%s"
        try:
            cursor.execute(sql, (user_id,))  # (user_id, ) - bo tworzymy krotkę
            data = cursor.fetchone()
        except Exception as e:
            print(f"Failed to select user {user_id} due to {e}")
            return None
        if data:
            loaded_user = User()
            loaded_user.__id = data[0]
            loaded_user.username = data[1]
            loaded_user.email = data[2]
            loaded_user.__hashed_password = data[3]
            return loaded_user
        else:
            return None

    @staticmethod
    def load_all_users(cursor):
        sql = "SELECT id, username, email, hashed_password FROM users"
        try:
            res = []
            cursor.execute(sql)
            for data in cursor:
                loaded_user = User()
                loaded_user.__id = data[0]
                loaded_user.username = data[1]
                loaded_user.email = data[2]
                loaded_user.__hashed_password = data[3]
                res.append(loaded_user)
            return res
        except Exception as e:
            print(f"Failed to select user {user_id} due to {e}")
            return []

