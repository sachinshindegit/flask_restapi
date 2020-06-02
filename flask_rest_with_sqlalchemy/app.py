from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from flask_rest_with_sqlalchemy.my_security import authenticate, identity
from flask_rest_with_sqlalchemy.resources.user import UserRegister, User
from flask_rest_with_sqlalchemy.resources.item import Item, ItemList
from flask_rest_with_sqlalchemy.db import db
from flask_rest_with_sqlalchemy.resources.store import Store, StoreList

application = Flask(__name__)
application.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///my_data.db'
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # This will turn off the Flask sqlalchemy modication tracker. We do this coz sqlalchemy has its own modification tracker which is better
application.config['PROPAGATE_EXCEPTIONS'] = True # This will propage any JWT related errors to Flask APP. If this is false, the flask app will be unaware of any jwt errors
application.secret_key = 'Sachin'
api = Api(application)

@application.before_first_request # This decorator will execute the following function before we get the first request
def create_tables():
    db.create_all() # This will create the database (my_data.db as mentioned above) and create the tables if they don't exist

jwt = JWT(application, authenticate, identity) # This will create a POST endpoint '/auth' as: http://127.0.0.1:5000/auth which will use authenticate and identity methods.
# It will return a jwt token.
# For the requests which have jwt_required(), need to pass jwt in headers with key as "AUTHORIZATION" and value as: JWT your_token

api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')
api.add_resource(Item, '/item/<string:name>') # http://127.0.0.1:5000/item, body-> {"name": name, "price":"23.3}
api.add_resource(ItemList, '/items') # http://127.0.0.1:5000/items, body-> {"name": name, "price":"23.3}
api.add_resource(UserRegister, '/register')
api.add_resource(User, '/user/<int:user_id>')

if __name__ == '__main__':
    db.init_app(application)
    application.run(port=5000, debug=True) # debug=True will add more info to the console when the server is running. If it is not needed then we can just have app.run(port=5000)