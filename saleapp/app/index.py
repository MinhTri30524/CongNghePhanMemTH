import math

from flask import render_template, request, redirect, jsonify, session
import dao
from app import app
import utils


@app.route("/")
def index():
    categories = dao.load_categories()

    page = request.args.get('page', 1)
    cate_id = request.args.get('category_id')
    kw = request.args.get('kw')
    products = dao.load_products(cate_id=cate_id, kw=kw, page=int(page))

    page_size = app.config["PAGE_SIZE"]
    total = dao.count_products()

    return render_template("index.html", cate=categories, prods=products, pages=math.ceil(total/page_size))


@app.route("/api/carts", methods=['post'])
def add_to_cart():
    """
    "1": {
        "id": "1",
        "name": "ABC",
        "price": 111,
        "quantity": 1
    },
    "2": {
        "id": "2",
        "name": "ABC",
        "price": 111,
        "quantity": 1
    }
    """

    cart = session.get('cart')
    if not cart:
        cart = {}

    id = str(request.json.get("id"))
    name = request.json.get("name")
    price = request.json.get("price")

    if id in cart:
        cart[id]["quantity"] += 1
    else:
        cart[id] = {
            "id": id,
            "name": name,
            "price": price,
            "quantity": 1
        }
    session['cart'] = cart

    print(cart)
    return jsonify(utils.stats_cart(cart))


@app.route("/register", methods=['get', 'post'])
def register_view():
    err_msg = ''
    if request.method.__eq__('POST'):
        password = request.form.get('password')
        confirm = request.form.get('confirm')

        if not password.__eq__(confirm):
            err_msg = 'Error Password'
        else:
            data = request.form.copy()

            del data['conform']
            dao.add_user(**data)
            return redirect('/login')

    return render_template("register.html", err_msg=err_msg)


if __name__ == '__main__':
    app.secret_key = 'super secret key'
    with app.app_context():
        app.run(debug=True)
