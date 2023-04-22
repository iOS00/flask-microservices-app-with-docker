from flask import Flask, jsonify, request
from db import db
from Product import Product

app = Flask(__name__)
# connect to MySQL 'products' database at db container with username-"root", pass-"password"
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:password@db/products'
db.init_app(app) # Flask-SQLAlchemy method to start sql db


# curl -v http://localhost:5000/products
@app.route('/products')
def get_products():
    products = [product.json for product in Product.find_all()]
    return jsonify(products)


# curl -v http://localhost:5000/product/1
@app.route('/product/<int:id>')
def get_product(id):
    product = Product.find_by_id(id)
    if product:
        return jsonify(product.json)  # remember to use jsonify on python dictionaries
    return f'Product with id {id} not found', 404

# curl --header "Content-Type: application/json" --request POST --data '{"name": "Product 3"}' -v http://localhost:5000/product
@app.route('/product', methods=['POST'])
def post_product():
    print ('POST /product')
    # Retrieve the product from the request body
    request_product = request.json

    # Create a new product
    product = Product(None, request_product['name'])  # remember None for autoincrement id field

    # Save the product to the database
    product.save_to_db()

    # Return the new product back to the client
    return jsonify(product.json), 201


# curl --header "Content-Type: application/json" --request PUT --data '{"name": "Updated Product 2"}' -v http://localhost:5000/product/2
@app.route('/product/<int:id>', methods=['PUT'])
def put_product(id):

    existing_product = Product.find_by_id(id)

    if existing_product:
        updated_product = request.json
        existing_product.name = updated_product['name']
        existing_product.save_to_db()

        return jsonify(existing_product.json), 200
    return f'Product with id {id} not found', 404


# curl --request DELETE -v http://localhost:5000/product/2
@app.route('/product/<int:id>', methods=['DELETE'])
def delete_product(id):
    existing_product = Product.find_by_id(id)
    if existing_product:
        existing_product.delete_from_db()
        return jsonify({
            'message': f'Product with id {id} deleted'
        }), 200

    return f'Product with id {id} not found', 404


if __name__ == '__main__':  # if it is the main script
    app.run(debug=True, host='0.0.0.0')  # to make visible for external computers, and outside docker
