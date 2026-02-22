from app import create_app 
from app.models import db
from flask import Flask # імпортуємо фласк
import os # імпортуємо ос, це бібліотека для роботи з файлами та директоріями


app=create_app() # створюємо додаток


if __name__ == '__main__':
    #create DB tables if not exist
    with app.app_context():
        db.create_all()
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)


#ttt
