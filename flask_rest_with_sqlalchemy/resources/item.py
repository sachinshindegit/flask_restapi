from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import jwt_required
from flask_rest_with_sqlalchemy.models.item import ItemModel
import sqlite3

class Item(Resource):

    @jwt_required() # This will mandate that we need to pass jwt which we generated using /auth endpoint seen above
    def get(self, name):
        data = request.get_json()
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        else:
            return {'item': None}, 404 # This will return 404 status along with the reposnse if the item is not found

    def post(self, name):
        data = request.get_json()
        item = ItemModel.find_by_name(name)
        if item:
            return {'Message': f'Item with name {name} already exists.'}, 400
        try:
            item = ItemModel(name, data['price'], data['store_id'])
            item.save_to_db()
        except:
            return {"Message": "Failed to insert the record in the db"}, 500

        return {"name": name, "price": data['price']}, 201

    def delete(selfs, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()

    def put(self, name):
        data = Item.parser.parse_args()

        item = ItemModel.find_by_name(data['name'])
        if item is None:
            item = ItemModel(name, data['price'], data['store_id'])
        else:
            item.price = data['price']

        item.save_to_db()

        return item.json(), 201

class ItemList(Resource):
    def get(self):
        return {'items': [item.json() for item in ItemModel.query.all()]}