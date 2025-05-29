from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

#データベースのテーブルを作成
class Post(db.Model):
    #id
    id = db.Column(db.Integer, primary_key=True)
    #タイトル
    title = db.Column(db.String, nullable=False)
    #内容
    content = db.Column(db.Text, nullable=False)
    #作成日時
    created_at = db.Column(db.DateTime, default=datetime.now)
