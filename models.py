from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# SQLAlchemyのインスタンスを作成
db = SQLAlchemy()

# Postモデル：投稿データを表すデータベースのテーブル
class Post(db.Model):
    # id：主キーとして設定
    id = db.Column(db.Integer, primary_key=True)
    # title：投稿のタイトル、空であってはならない
    title = db.Column(db.String, nullable=False)
    # content：投稿の内容、空であってはならない
    content = db.Column(db.Text, nullable=False)
    # created_at：投稿の作成日時、デフォルトで現在時刻が設定される
    created_at = db.Column(db.DateTime, default=datetime.now)
