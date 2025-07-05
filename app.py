from flask import Flask, render_template, request, redirect, url_for
from models import db, Post

# Flaskアプリケーションのインスタンスを作成
app = Flask(__name__)
# SQLAlchemyのデータベースURIを設定
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"
# SQLAlchemyをアプリケーションに初期化
db.init_app(app)

# ルーティング

# トップページ：投稿の一覧を表示
@app.route('/')
def index():
  # データベースからすべての投稿を作成日時の降順で取得
  posts = Post.query.order_by(Post.created_at.desc()).all()
  # index.htmlをレンダリングし、投稿データを渡す
  return render_template('index.html', posts=posts)


# 新規投稿ページ：GETリクエストの場合はフォームを表示、POSTリクエストの場合は投稿を作成
@app.route('/create', methods=['GET', 'POST'])
def create():
  # POSTリクエストの場合
  if request.method == 'POST':
    # フォームからタイトルと内容を取得
    title = request.form.get('title')
    content = request.form.get('content')
    # 新しい投稿オブジェクトを作成
    post = Post(title=title, content=content)
    # データベースセッションに新しい投稿を追加
    db.session.add(post)
    # データベースに変更をコミット
    db.session.commit()
    # トップページにリダイレクト
    return redirect(url_for('index'))
  # GETリクエストの場合は新規投稿ページを表示
  return render_template('create.html')


# 投稿削除機能：指定されたIDの投稿を削除
@app.route("/delete/<int:id>",methods=["GET"])
def delete(id):
  # 指定されたIDの投稿をデータベースから取得
  post = Post.query.get(id)
  # データベースセッションから投稿を削除
  db.session.delete(post)
  # データベースに変更をコミット
  db.session.commit()
  # トップページにリダイレクト
  return redirect(url_for('index'))


# 投稿編集ページ：GETリクエストの場合はフォームを表示、POSTリクエストの場合は投稿を更新
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
  # 指定されたIDの投稿をデータベースから取得
  post = Post.query.get(id)
  # POSTリクエストの場合
  if request.method == 'POST':
    # フォームから新しいタイトルと内容を取得（空の場合は既存の値を維持）
    post.title = request.form.get('title') if request.form.get('title')!="" else post.title
    post.content = request.form.get('content') if request.form.get('content')!="" else post.content
    # データベースに変更をコミット
    db.session.commit()
    # トップページにリダイレクト
    return redirect(url_for('index'))
  # GETリクエストの場合は編集ページを表示
  return render_template('edit.html', post=post)


# スクリプトが直接実行された場合にアプリケーションを起動
if __name__ == '__main__':
    # デバッグモードでアプリケーションを実行
    app.run(debug=True)
