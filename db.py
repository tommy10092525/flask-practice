from app import app,db

# アプリケーションコンテキスト内でデータベースのテーブルを作成
with app.app_context():
    # すべてのモデル（テーブル）を作成
    db.create_all()
    # データベースに変更をコミット
    db.session.commit()
