from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_with_jwt_extended.resources.user import UserRegister, User, UserLogin, TokenRefresh
from flask_with_jwt_extended.resources.item import Item, ItemList
from flask_with_jwt_extended.db import db
from flask_with_jwt_extended.resources.store import Store, StoreList

application = Flask(__name__)
application.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///my_data.db'
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # This will turn off the Flask sqlalchemy modication tracker. We do this coz sqlalchemy has its own modification tracker which is better
application.config['PROPAGATE_EXCEPTIONS'] = True # This will propage any JWT related errors to Flask APP. If this is false, the flask app will be unaware of any jwt errors
application.secret_key = 'Sachin'
application.config['JWT_SECRET_KEY'] = 'sachin_jwt_secret'


api = Api(application)

@application.before_first_request # This decorator will execute the following function before we get the first request
def create_tables():
    db.create_all() # This will create the database (my_data.db as mentioned above) and create the tables if they don't exist

jwt = JWTManager(application)

@jwt.user_claims_loader
def add_claims_to_jwt(identity):
    if identity == 1: # Instead of hardcoding it here, you should read from config or database
        return {'is_admin': True}
    return {'is_admin': False}

@jwt.expired_token_loader
def expired_token_callback():
    # This method would be called if an expired token is used to make a request
    return jsonify({
        'Message': 'This token has expired',
        'error': 'token_expired'
    }), 401


api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')
api.add_resource(Item, '/item/<string:name>') # http://127.0.0.1:5000/item, body-> {"name": name, "price":"23.3}
api.add_resource(ItemList, '/items') # http://127.0.0.1:5000/items, body-> {"name": name, "price":"23.3}
api.add_resource(UserRegister, '/register')
api.add_resource(User, '/user/<int:user_id>')
api.add_resource(UserLogin, '/login')
api.add_resource(TokenRefresh, '/refresh')

if __name__ == '__main__':
    db.init_app(application)
    application.run(port=5000, debug=True) # debug=True will add more info to the console when the server is running. If it is not needed then we can just have app.run(port=5000)