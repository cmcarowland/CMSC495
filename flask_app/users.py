'''
Golden Hour App Group 1
UMGC CMSC 495 7385
Shivam Patel, Raymond Rowland, Mariam Ahmed, Katrina Wilhelm, Paul Cooper
November 5, 2025

users.py

Defines the Users class for managing multiple User objects.
Loads and saves user data from JSON, manages authentication,
and creates or retrieves users.
'''

from flask_app.user import User

import json
import os

class Users:
    """
    Class to manage multiple User instances.
    Handles loading from and saving to a JSON file.
    """

    FILENAME : str = './data/users.json'
    NEXT_ID : int = 1

    def __init__(self):
        """
        Initialize the Users manager.
        Loads users from a JSON file if it exists.
        """

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
        """
        Get the next available user ID.
        Returns:
            int: The next user ID.
        """

        nid = Users.NEXT_ID
        Users.NEXT_ID += 1
        return nid

    def save(self):
        """
        Save the current users to the JSON file.
        Returns:
            None
        """

        with open(Users.FILENAME, 'w', encoding='utf-8') as ofile:
            users = [user.to_json() for user in self.users]
            json.dump({"NEXT_ID": Users.NEXT_ID, "users": users}, ofile, indent=4)

    def get_user(self, email) -> User | None:
        """
        Get a user by their email.
        Args:
            email (str): The email of the user.
        Returns:
            User | None: The user object if found, otherwise None.
        """

        user = next(filter(lambda x: x.email == email, self.users), None)

        if user is not None:
            return user

        return None
    
    def get_user_by_id(self, id) -> User | None:
        """
        Get a user by their ID.
        Args:
            id (int): The ID of the user.
        Returns:
            User | None: The user object if found, otherwise None.
        """

        user = next(filter(lambda x: x.id == id, self.users), None)

        if user is not None:
            return user

        return None

    def add_user(self,  email : str, user_name : str, pw : str) -> bool:
        """
        Add a new user.
        Args:
            email (str): The email of the user.
            user_name (str): The username.
            pw (str): The password.
        Returns:
            bool: True if the user was added, False if the user already exists.
        """

        user = self.get_user(email)
        if user:
            return False
        
        user = User(email, user_name, pw)
        user.id = Users.get_next_id()

        self.users.append(user)
        self.save()
        return True

    def login(self, email : str, pw : str) -> bool:
        """
        Attempt to log in a user.
        Args:
            email (str): The email of the user.
            pw (str): The password.
        Returns:
            bool: True if login is successful, False otherwise.
        """
        
        user = self.get_user(email)
        if not user:
            return False

        if pw != user.password_hash:
            return False

        return True