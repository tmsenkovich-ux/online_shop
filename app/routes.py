from flask import Blueprint, render_template, request, redirect, url_for, flash
from .models import db, Product

bp=Blueprint('routes', __name__) # створюємо блупринт


@bp.route('/') # головна сторінка
def index():
    return render_template('index.html') # повертаємо html сторінку

@bp.route('/product') # сторінка з продуктами
def products():
    products=Product.query.all() # отримуємо всі продукти з бази даних
    return render_template('product_list.html', products=products) # повертаємо нову html сторінку з продуктами
# блупринт розділяє код на малі частинки щоб було легше з ним працювати

# потім ми імпортуєило бп в ініт пай

@bp.route('/add', methods=['GET', 'POST'])  # сторінка для додавання продукту
def add_product():
    if request.method == 'POST':
        name =request.form['name']
        price = float(request.form['price'])
        product=Product(name=name, price=float(price))
        db.session.add(product)
        db.session.commit()
        flash('Product added')
        return redirect(url_for('routes.products'))
    return render_template('product_form.html', action='Add', product=None)    
