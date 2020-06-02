from flask_restful import Resource
from flask_with_jwt_extended.models.store import StoreModel

class Store(Resource):
    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json()
        return {'Message': 'Store not found'}, 404


    def post(self, name):
        if StoreModel.find_by_name(name):
            return {'Message': 'A store with name {} already exists'.format(name)}

        store = StoreModel(name)
        try:
            store.save_to_db()
        except:
            return {'Messge': 'An error occurred while creating the store'}

    def delete(self, name):
        store =  StoreModel.find_by_name(name)
        if store is None:
            return {'Message': 'A store with name {} already exists'.format(name)}
        else:
            store.delete_from_db()
        return {'Messge': 'Store deleted successfully'}

class StoreList(Resource):
    def get(self):
        return {'stores': [store.json() for store in StoreModel.query.all()]}
