from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required
from simple_flask_restful_app.my_security import authenticate, identity

app = Flask(__name__)
app.secret_key = 'Sachin'
api = Api(app)

jwt = JWT(app, authenticate, identity) # This will create a POST endpoint '/auth' to which we need to pass username and password. It will return a jwt token.
# For the requests which have jwt_required(), need to pass jwt in headers with key as "AUTHORIZATION" and value as: JWT your_token

# Every Restful API should have resource which can be returned.
# Every resource should have a class
# Every resource class should inherit from Resource

items = {
        'chair': {'name': 'chair', 'price': 12.00}
    }

# Creating Student Resource.
class Item(Resource):

    @jwt_required() # This will mandate that we need to pass jwt which we generated using /auth endpoint seen above
    def get(self, name):
        # defining 'get' method which will be called on GET request
        item = items.get(name, None)
        if item:
            return item
        return {'item': None}, 404 # This will return 404 status along with the reposnse if the item is not found

    def post(self, name):
        if name in items:
            return {'Message': f'Item with name {name} already exists.'}, 400
        data = request.get_json()
        item = {'name': name, 'price': data['price']}
        items[name] = item
        return item, 201

    def put(self, name):
        # Using reqparse to parse through the incoming request params.
        parser = reqparse.RequestParser()
        parser.add_argument('price',
                            type = float,
                            required = True, # Making 'price' as mandatory
                            help = 'This field cannot be left blank'
                            )
        data = parser.parse_args()
        item = items.get(name, None)
        if item:
            item['price'] = data['price']
            items[name] = item

        return item


class ItemList(Resource):

    def get(self):
        return {'Items': items}

api.add_resource(Item, '/item/<string:name>') # http://127.0.0.1:5000/item/chair
api.add_resource(ItemList, '/item')

if __name__ == '__main__':
    app.run(port=5000, debug=True) # debug=True will add more info to the console when the server is running. If it is not needed then we can just have app.run(port=5000)