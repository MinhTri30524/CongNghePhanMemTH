from flask import render_template, request
import dao
from app import app


@app.route("/")
def index():
    categories = dao.load_categories()
    cate_id = request.args.get('category_id')
    products = dao.load_products(cate_id=cate_id)

    return render_template("index.html", cate=categories, prods=products)


if __name__ == '__main__':
    app.run(debug=True)
