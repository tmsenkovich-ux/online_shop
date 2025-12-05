from flask import Blueprint, render_template
from .models import db, Product

bp=Blueprint('routes', __name__) # створюємо блупринт


@bp.route('/') # головна сторінка
def index():
    return render_template('index.html') # повертаємо html сторінку

@bp.route('/products') # сторінка з продуктами
def products():
    products=Product.query.all() # отримуємо всі продукти з бази даних
    return render_template('products.html', products=products) # повертаємо нову html сторінку з продуктами
# блупринт розділяє код на малі частинки щоб було легше з ним працювати

# потім ми імпортуєило бп в ініт пай


