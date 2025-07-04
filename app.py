from flask import Flask, render_template, request, redirect, url_for
from models import db, Post

# アプリケーションの設定
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"
db.init_app(app)

# ルーティング

@app.route('/')
def index():
  # 投稿一覧を取得
  posts = Post.query.order_by(Post.created_at.desc()).all()
  # 投稿一覧を表示
  return render_template('index.html', posts=posts)


@app.route('/create', methods=['GET', 'POST'])
def create():
  if request.method == 'POST':
    # フォームからデータを取得
    title = request.form.get('title')
    content = request.form.get('content')
    # データベースに保存
    post = Post(title=title, content=content)
    db.session.add(post)
    db.session.commit()
    # 投稿一覧にリダイレクト
    return redirect(url_for('index'))
  # 投稿フォームを表示
  return render_template('create.html')


@app.route("/delete/<int:id>",methods=["GET"])
def delete(id):
  post = Post.query.get(id)
  db.session.delete(post)
  db.session.commit()
  return redirect(url_for('index'))


@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
  post = Post.query.get(id)
  if request.method == 'POST':
    # フォームからデータを取得
    post.title = request.form.get('title') if request.form.get('title')!="" else post.title
    post.content = request.form.get('content') if request.form.get('content')!="" else post.content
    # データベースに保存
    db.session.commit()
    # 投稿一覧にリダイレクト
    return redirect(url_for('index'))
  # 編集フォームを表示
  return render_template('edit.html', post=post)


if __name__ == '__main__':
    app.run(debug=True)
