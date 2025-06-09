from app import app,db
# データベースのテーブルを作成
with app.app_context():
    db.create_all()
    db.session.commit()
