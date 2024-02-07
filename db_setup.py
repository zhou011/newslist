# 文件路径：/your/project/path/db_setup.py

from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

def init_app(app):
    db.init_app(app)