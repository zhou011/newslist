# 文件路径：/your/project/path/models.py

from db_setup import db
import datetime

class News(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    platform = db.Column(db.String(50), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    link = db.Column(db.String(200), nullable=False)
    hot_topic = db.Column(db.String(200), nullable=True) # 根据需要可以指定 string 最大长度

    def __repr__(self):
        return f'<News {self.id} {self.title}>'

class PlatformList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    platform_name = db.Column(db.String(50), nullable=False, unique=True)