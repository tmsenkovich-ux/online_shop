from flask_sqlalchemy import SQLAlchemy # імпортуємо SQLAlchemy для роботи з базою даних

# це бібліотека для роботи з базами даних в об'єктно-реляційній манері

db=SQLAlchemy() # створюємо об'єкт бази даних

class Product(db.Model): # модель продукту
    __tablename__='products' # назва таблиці
    id=db.Column(db.Integer, primary_key=True, autoincrement=True) # унікальний ідентифікатор
    name=db.Column(db.String(100), nullable=False) # назва продукту
    price=db.Column(db.Float, nullable=False) # ціна продукту
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())
    description=db.Column(db.Text, nullable=True) # опис продукту
    