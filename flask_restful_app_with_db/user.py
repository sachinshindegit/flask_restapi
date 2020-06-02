import sqlite3
from flask_restful import Resource, reqparse

class User:
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    @classmethod
    def find_by_username(cls, username, password):
        connection = sqlite3.connect('./database/my_data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM users WHERE username = ? and password = ?"
        result = cursor.execute(query, (username,password))
        row = result.fetchone()
        if row:
            user = cls(*row)
        else:
            user = None

        connection.close()
        return user

    @classmethod
    def find_by_userid(cls, _id):
        connection = sqlite3.connect('./database/my_data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM users WHERE id = ?"
        result = cursor.execute(query, (_id,))
        row = result.fetchone()
        if row:
            user = cls(*row)
        else:
            user = None

        connection.close()
        return user

class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str,
                        required=True,  # Making 'username' as mandatory
                        help='This field cannot be left blank'
                        )
    parser.add_argument('password',
                        type=str,
                        required=True,  # Making 'username' as mandatory
                        help='This field cannot be left blank'
                        )
    def post(self):
        connection = sqlite3.connect('./database/my_data.db')
        cursor = connection.cursor()
        data = UserRegister.parser.parse_args()
        query = "INSERT INTO users VALUES (NULL, ?, ?)"
        cursor.execute(query, (data['username'], data['password'],))
        connection.commit()
        connection.close()
        return {'Message': 'User created successfully'}