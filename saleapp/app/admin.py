from app.models import Category, Product, User
from flask_admin.contrib.sqla import ModelView
from flask_admin import Admin
from app import app, db

class ProductView(ModelView):


admin = Admin(app=app, name='eCommerce Admin', template_mode='bootstrap4')
admin.add_view(ModelView(Category, db.session))
admin.add_view(ModelView(Product, db.session))
admin.add_view(ModelView(User, db.session))