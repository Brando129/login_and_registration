from flask_app.config.mysqlconnection import connectToMySQL
# Flash messages import
from flask import flash
# REGEX import
import re
# Create a regular expression object that we'll use later
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

# Database name
db = "login_and_registration_schema"

# User class
class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']

    # Classmethod for saving a new user.
    @classmethod
    def save(cls, data):
        query = """ INSERT INTO users (first_name, last_name, email, password)
                VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);"""
        return connectToMySQL(db).query_db(query, data)

    # Staticmethod for validating a user.
    @staticmethod
    def validate_user(data):
        is_valid = True
        if len(data['first_name']) < 2:
            flash("First name is required.", "register")
            is_valid = False

        if len(data['last_name']) < 2:
            flash("Last name is required.", "register")
            is_valid = False

        # Test whether email matches the  EMAIL_REGEX pattern
        if not EMAIL_REGEX.match(data['email']):
            flash("Invalid email address!" , "register")
            is_valid = False
        query = """SELECT * FROM users
                WHERE email = %(email)s;"""
        results = connectToMySQL(db).query_db(query, data)

        if len(results) != 0:
            flash("This email is already being used.", "register")
            is_valid = False

        if len(data['password']) < 8:
            flash("Password is must be at least 8 characters.", "register")
            is_valid = False


        if data['password'] != data['confirm_password', "register"]:
            flash("Password does not match.")
            is_valid = False
        return is_valid