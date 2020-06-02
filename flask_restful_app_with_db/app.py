from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from flask_restful_app_with_db.my_security import authenticate, identity
from flask_restful_app_with_db.user import UserRegister
from flask_restful_app_with_db.item import Item, ItemList

application = Flask(__name__)
application.secret_key = 'Sachin'
api = Api(application)

jwt = JWT(application, authenticate, identity) # This will create a POST endpoint '/auth' as: http://127.0.0.1:5000/auth which will use authenticate and identity methods.
# It will return a jwt token.
# For the requests which have jwt_required(), need to pass jwt in headers with key as "AUTHORIZATION" and value as: JWT your_token

api.add_resource(Item, '/item') # http://127.0.0.1:5000/item, body-> {"name": name, "price":"23.3}
api.add_resource(ItemList, '/items') # http://127.0.0.1:5000/items, body-> {"name": name, "price":"23.3}
api.add_resource(UserRegister, '/register')

if __name__ == '__main__':
    application.run(port=5000, debug=True) # debug=True will add more info to the console when the server is running. If it is not needed then we can just have app.run(port=5000)