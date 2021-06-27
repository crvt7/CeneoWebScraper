from flask.helpers import send_file
from app import app
from app.models.product import Product
from flask import render_template, redirect, url_for, request
from os import listdir
import json

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html.jinja')

@app.route('/extract', methods=['GET', 'POST'])
def extract():
    if request.method == 'POST':
        product_id = request.form.get('product_id')
        product = Product(product_id)
        product.extract_product()
        if product.product_name == "empty_product_name":
            return render_template('extractError.html.jinja')
        product.save_to_json()
        product.create_json_stats()
        return redirect(url_for('opinions', product_id=product_id))
    return render_template('extract.html.jinja')


@app.route('/products')
def products():
    products_list = [product.split('.')[0] for product in listdir("app/products")]
    stats = {}
    for file in listdir("app/stats"):
        with open(f"app/stats/{file}", "r", encoding="UTF-8") as fp:
            f = json.load(fp)
            stats[f["id"]] = f
    return render_template('products.html.jinja', stats=stats, products=products_list)

@app.route('/opinions/<product_id>')
def opinions(product_id):
    print(product_id)
    product = Product(product_id)
    print(", ".join(op.opinion_id for op in product.opinions))
    product.read_from_json()
    return render_template('opinions.html.jinja', product=str(product))

@app.route('/charts/<productId>')
def charts(product_id):
    pass

@app.route('/about')
def about():
    return render_template('about.html.jinja')

@app.route('/download/<file_name>')
def download_file(file_name):
    path = app.root_path + "/products/" + file_name + ".json"
    return send_file(path, as_attachment=True)