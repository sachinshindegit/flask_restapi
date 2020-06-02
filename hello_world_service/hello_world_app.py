from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello World"

stores = [
    {
        'name': 'My store',
        'items': [
            {
                'name': 'My item',
                'price': 15.99
            }
        ]
    }
]
@app.route('/store', methods=['POST'])
def create_store():
    request_data = request.get_json()
    new_store = {
        'name': request_data['name'],
        'items': []
    }
    stores.append(new_store)

    return jsonify(new_store)


@app.route('/store') # Default method is GET
def get_stores():
    return jsonify({'stores': stores})


@app.route('/store/<string:name>')
def get_store(name):
    for store in stores:
        if store['name'] == name:
            return jsonify({'Store': store})

    return jsonify({'message': f'{name} store not found'})

@app.route('/store/<string:name>/item', methods=['POST'])
def create_item_in_store(name):
    request_data = request.get_json()
    for store in stores:
        if store['name'] == name:
            store['items'].append({
                'name': request_data['item_name'],
                'price': request_data['item_price']
            })
            return jsonify({'Store': store['items']})

    return jsonify({'message': f'{name} store not found'})


@app.route('/store/<string:name>/item')
def get_items_in_store(name):
    for store in stores:
        if store['name'] == name:
            return jsonify({'Store': store['items']})

    return jsonify({'message': f'{name} store not found'})


app.run(port=5000)