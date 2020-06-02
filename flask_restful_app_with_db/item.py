from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import jwt_required
import sqlite3

class Item(Resource):

    @classmethod
    def find_by_name(cls, name):
        connection = sqlite3.connect('./database/my_data.db')
        cursor = connection.cursor()
        query = "SELECT * FROM items WHERE name = ?"
        result = cursor.execute(query, (name,))
        row = result.fetchone()
        connection.commit()
        connection.close()

        if row:
            return {'item': {'name': row[0], 'price': row[1]}}
        else:
            return None

    @jwt_required() # This will mandate that we need to pass jwt which we generated using /auth endpoint seen above
    def get(self, name):
        data = request.get_json()
        item = Item.find_by_name(name)
        if item:
            return item
        else:
            return {'item': None}, 404 # This will return 404 status along with the reposnse if the item is not found

    def post(self, name):
        data = request.get_json()
        item = Item.find_by_name(name)
        if item:
            return {'Message': f'Item with name {name} already exists.'}, 400
        try:
            connection = sqlite3.connect('./database/my_data.db')
            cursor = connection.cursor()
            query = "INSERT INTO items VALUES (?, ?)"
            cursor.execute(query, (name, data['price'],))
            connection.commit()
        except:
            return {"Message": "Failed to insert the record in the db"}, 500
        finally:
            connection.close()

        return {"name": name, "price": data['price']}, 201

    def put(self, name):
        # Using reqparse to parse through the incoming request params.
        parser = reqparse.RequestParser()
        parser.add_argument('price',
                            type = float,
                            required = True, # Making 'price' as mandatory
                            help = 'This field cannot be left blank'
                            )
        parser.add_argument('name',
                            type=str,
                            required=True,  # Making 'price' as mandatory
                            help='This field cannot be left blank'
                            )
        data = parser.parse_args()

        connection = sqlite3.connect('./database/my_data.db')
        cursor = connection.cursor()
        query = "UPDATE items SET price = ? WHERE name = ?"
        cursor.execute(query, (data['price'], data['name'],))
        connection.commit()
        connection.close()

        return {"name": data['name'], "price": data['price']}, 201

class ItemList(Resource):
    def get(self):
        connection = sqlite3.connect('./database/my_data.db')
        cursor = connection.cursor()
        query = "SELECT * from items"
        result = cursor.execute(query)

        items = []
        for row in result:
            items.append({'name': row[0], 'price': row[1]})

        connection.close()
        return {'items': items}