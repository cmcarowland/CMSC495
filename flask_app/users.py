from flask_app.user import User

import json
import os

class Users:
    FILENAME : str = 'users.json'

    def __init__(self):
        self.users = []
        self.authenticated = {}

        if os.path.exists(Users.FILENAME):
            with open(Users.FILENAME, 'r', encoding='utf-8') as ifile:
                for user_data in json.load(ifile)['users']:
                    user = User.from_json(user_data)
                    self.users.append(user)

    def save(self):
        with open(Users.FILENAME, 'w', encoding='utf-8') as ofile:
            users = [user.to_json() for user in self.users]
            json.dump({"users": users}, ofile, indent=4)

    def get_user(self, user_name) -> User | None:
        user = list(filter(lambda x: x.user_name == user_name, self.users))

        if len(user) == 1:
            return user[0]

        return None

    def add_user(self, user_name : str, pw : str) -> bool:
        user = self.get_user(user_name)
        if user:
            return False
        
        user = User(user_name, pw)

        self.users.append(user)
        self.save()
        return True

    def login(self, user_name : str, pw : str) -> bool:
        user = self.get_user(user_name)
        if not user:
            return False

        if pw != user.password_hash:
            return False

        return True