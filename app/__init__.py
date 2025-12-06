from flask import Flask # імпортуємо фласк
import json
import os
import sqlite3


def create_app(): # створюємо додаток
    base_dir=os.path.abspath(os.path.dirname(__file__)+ '/..')
    app = Flask(__name__, template_folder=os.path.join(base_dir, 'templates'), # вказуємо шлях до папки з шаблонами, щоби Фласк міг спокійно і без перешкод їх знайти
                static_folder=os.path.join(base_dir, 'static'))
    
    
    # Load config from JSON file

    config_path = os.path.join(base_dir, 'config.json') #
    with open(config_path) as f:
        config = json.load(f)
    app.config.update(config)
    # Set up SQLAlchemy with absolute DB path
    db_path = os.path.abspath(os.path.join(base_dir, config['DB_PATH']))
    # Ensure the DB directory exists so SQLite can create the file
    db_dir = os.path.dirname(db_path)
    if not os.path.exists(db_dir):
        os.makedirs(db_dir, exist_ok=True)
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{db_path}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    _ensure_columns(db_path, 'products', {'created_at': 'DATETIME', 'updated_at': 'DATETIME'})

    
    
    from .models import db
    db.init_app(app)


    from .routes import bp as routes_bp   # імпортуємо блупринт
    app.register_blueprint(routes_bp) # реєструємо блупринт в додатку
    return app   # повертаємо створений додаток


def _ensure_columns(sqlite_path, table, columns):
    """Ensure the given columns exist on the SQLite table; add them if missing.


    This updates the SQLite file in-place (no backup) as requested.
    """
    if not os.path.exists(sqlite_path):
        return
    conn = sqlite3.connect(sqlite_path)
    cur = conn.cursor()
    try:
        cur.execute(f"PRAGMA table_info('{table}')")
        existing = {row[1] for row in cur.fetchall()}  # row[1] is column name
        for col, col_type in columns.items():
            if col not in existing:
                stmt = f"ALTER TABLE {table} ADD COLUMN {col} {col_type};"
                try:
                    cur.execute(stmt)
                except Exception:
                    # ignore errors to keep startup resilient
                    pass
        # After adding missing columns, ensure existing rows do not have NULL timestamps
        # Use SQLite CURRENT_TIMESTAMP to set current date/time for NULL values
        try:
            if 'created_at' in columns:
                cur.execute(f"UPDATE {table} SET created_at = CURRENT_TIMESTAMP WHERE created_at IS NULL;")
            if 'updated_at' in columns:
                cur.execute(f"UPDATE {table} SET updated_at = CURRENT_TIMESTAMP WHERE updated_at IS NULL;")
        except Exception:
            # ignore update errors; keep startup resilient
            pass
        conn.commit()
    finally:
        cur.close()
        conn.close()
