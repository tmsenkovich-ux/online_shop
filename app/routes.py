from flask import Blueprint, render_template, request, redirect, url_for, flash
from .models import db, Product

bp=Blueprint('routes', __name__) # створюємо блупринт


@bp.route('/') # головна сторінка
def index():
    products=Product.query.all() # отримуємо всі продукти з бази даних
    return render_template('index.html', products=products) # повертаємо html сторінку
                                       

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
              
        description=request.form['description']
        stock=request.form['stock']
        is_active = request.form.get("is_active") == 'on' 
        category=request.form['category']
        rating=(request.form['rating'])
        sale=int(request.form.get('sale')== 'on')
        product=Product(name=name, price=float(price), description=description, stock=stock, is_active=is_active, category=category, rating=rating, sale=sale ) 
        db.session.add(product)
        db.session.commit()
        flash('Product added')
        return redirect(url_for('routes.products'))
    return render_template('product_form.html', action='Add', product=None)      



@bp.route('/delete/<int:product_id>', methods=['POST'])
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    flash('Product deleted!')
    return redirect(url_for('routes.products'))

@bp.route('/update/<int:product_id>', methods=['GET', 'POST'])
def update_product(product_id):
    product = Product.query.get_or_404(product_id)
    if request.method=='POST':
        product.name = request.form['name']
        product.price = float(request.form['price'])
        product.description=request.form['description']
        product.stock=request.form['stock']
        product.is_active = request.form.get("is_active") == 'on'
        
        product.category=request.form['category']
        product.rating=request.form['rating']
        product.sale = request.form.get('sale') == 'on'

        print (f'''name={product.name}, price={product.price}, description={product.description}, stock={product.stock},
        is_active={product.is_active}, category={product.category}, rating={product.rating}, sale={product.sale}''')

        db.session.commit()
        flash('Product updated!')
        return redirect(url_for('routes.products'))
        
    return render_template('product_form.html', action='Add', product=product)          

   # db.session.delete(product)
   # db.session.commit()
    #flash('Product deleted!')
    #return redirect(url_for('routes.products'))