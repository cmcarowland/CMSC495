from flask_app.user import User

import json
import os

class Users:
    FILENAME : str = './data/users.json'
    NEXT_ID : int = 1

    def __init__(self):
        self.users = []
        self.authenticated = {}

        if os.path.exists(Users.FILENAME):
            with open(Users.FILENAME, 'r', encoding='utf-8') as ifile:
                data = json.load(ifile)
                Users.NEXT_ID = data.get("NEXT_ID", Users.NEXT_ID)
                for user_data in data['users']:
                    user = User.from_json(user_data)
                    self.users.append(user)

    @staticmethod
    def get_next_id() -> int:
        nid = Users.NEXT_ID
        Users.NEXT_ID += 1
        return nid

    def save(self):
        with open(Users.FILENAME, 'w', encoding='utf-8') as ofile:
            users = [user.to_json() for user in self.users]
            json.dump({"NEXT_ID": Users.NEXT_ID, "users": users}, ofile, indent=4)

    def get_user(self, email) -> User | None:
        user = next(filter(lambda x: x.email == email, self.users), None)

        if user is not None:
            return user

        return None
    
    def get_user_by_id(self, id) -> User | None:
        user = next(filter(lambda x: x.id == id, self.users), None)

        if user is not None:
            return user

        return None

    def add_user(self,  email : str, user_name : str, pw : str) -> bool:
        user = self.get_user(email)
        if user:
            return False
        
        user = User(email, user_name, pw)
        user.id = Users.get_next_id()

        self.users.append(user)
        self.save()
        return True

    def login(self, email : str, pw : str) -> bool:
        user = self.get_user(email)
        if not user:
            return False

        if pw != user.password_hash:
            return False

        return True