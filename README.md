# Flaskとデータベースを連携して、簡単なWebアプリを作ってみよう

## はじめに

SNSを作るにあたってはユーザのデータを保存するためのサーバが必要です。  
PythonでWebサーバを作るためのフレームワークである**Flask**を使って簡単な掲示板を作ってみましょう。  
コードの書き方を覚えるというよりもそのコードが持つ「意味」や「内容」に着目して全体の流れをつかむことを意識してください。細かい書き方は本質的でないので覚えなくて大丈夫です。  
FlaskはPythonのWebフレームワークの中でも特にシンプルで学習コストが低いものです。
Flaskを使うことでWebアプリケーションの開発を簡単に始めることができます。

## 各ファイルを作成して概要をつかもう

※必要なライブラリをインストールしていない場合は以下のコマンドを実行してください

```shell
pip install flask flask_sqlalchemy
```

- 必要なファイルを作成する
  - `app.py`、`models.py`、`db.py`をつくる
  - `templates`フォルダを作る
  - `templates`フォルダの中に`create.html`、`index.html`、`edit.html`を作る
- データベースを作成する
  - `db.py`を実行する
    - `python db.py`で実行
  - `instance/database.db`が作成されたことを確認する
- アプリケーションを起動する
  - `python app.py`でアプリを起動してブラウザで確認する[localhost](http://127.0.0.1:5000/)。

**sqlalchemy**:データベースをPythonのオブジェクトとして定義する**ORM**のひとつ

## 各ファイルについて

`app.py`アプリケーションの本体

`models.py`データベースのモデル定義

`db.py`データベースを作成する

`index.html`投稿一覧のHTML

`create.html`投稿作成のHTML

`edit.html`投稿編集のHTML

### アプリケーションを起動する

```shell
python app.py
```

```python
# python
if __name__ == '__main__':
    app.run(debug=True)
```

が実行されてテストサーバーが動きます

### データベースを作成する

```shell
python db.py
```

`models.py`にあるデータベースの定義からデータベースを作成します。

## ルーティングについて

### 基本的なルーティングの書き方

```python
# python
from flask import Flask
app = Flask(__name__)
@app.route('/')
def index():
    return "<p>こんにちは!</p>"

if __name__ == '__main__':
    app.run(debug=True)
```

このように書いて実行するとWebサーバーが立ち上がり、URLのアクセスに対してレスポンスを返すことができます
`@app.route('/')`の@はデコレータと呼びます。（難しいから書き方だけ覚えればＯＫ！）
デコレータは関数に対して特別な処理を追加するためのPythonの機能です。  
`@app.route('/')`は「この関数は`/`というURLにアクセスしたときに実行される」という意味です。
`index()`関数は`/`にアクセスしたときに実行される関数で、ここでは`"<p>こんにちは!</p>"`というHTMLを返しています。

###　動的なルーティング
```python
# python
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
```

`@app.route('/edit/<int:id>', methods=['GET', 'POST'])`について、`/edit/<int:id>`は`/edit/`の後に数字があるURLに対応することを示しています。`<int:id>`のURLの部分の数字を`def edit(id):`の引数のidとして利用しています。  
`methods=['GET', 'POST']`は`GET`と`POST`のリクエストを許可するという意味です。`method`が`GET`であれば投稿編集用のページを返し、`POST`であればフォームに含まれる`title`と`content`を取り出し、投稿の内容を更新しています。



## データベースについて

### 概要

投稿はデータベースという仕組みを使って管理します。
データベースを利用すると形式を決めて整理してデータを管理することができます。

```python
# python
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
```

表形式でデータを格納することができます  
↓イメージ

|id| title|content|created_at|
|-|-|-|-|
|1|今日は池袋の水族館に行った|ペンギンがかわいかった|2025-07-02|
|2|今日は大学に行った|とても暑かった|2025-07-02|
|...|...|...|...|

本来データベースを操作するには **SQL**というデータベース操作言語を使います。しかし、独特な記法で習得が難しいです。
Pythonをはじめとした多くの言語には**ORM**という仕組みが用意されていてSQLを使わずともそのプログラミング言語の書き方でデータベースを操作することができます。
Flaskアプリケーションでデータベースを扱う際には**flask_sqlalchemy**というライブラリを使ってデータベースをPythonの書き方で操作することができます。
SQLAlchemyはPythonのORMの一つで、Flaskと組み合わせて使うことができます。
  
「投稿一覧を作成日時の降順で取得する」という場合には以下のようになります。（覚える必要はありません）

#### SQLの場合

```sql
-- sql
SELECT * FROM POSTS ORDER BY created_at DESC
```

#### Pythonの場合

```python
# python
posts = Post.query.order_by(Post.created_at.desc()).all()
```

`DESC`はdescendの略で降順を意味します


### SQLite

```python
# python
# アプリケーションの設定
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"
db.init_app(app)
```

[SQLite](https://sqlite.org/)というデータベースのソフトウェアの形式でデータベースを作成・管理しています。  
`app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"`にて「このアプリケーションでデータベースでSQLiteを使う」という設定をしています。この部分を書き換えることで簡単にほかのデータベースも利用することができます。
`sqlite:///database.db`はSQLiteのデータベースファイルのパスを指定しています。
`db.init_app(app)`でアプリケーションにデータベースを初期化します。


### フォームのデータをデータベースに格納する

```python
# python
# フォームからデータを取得
if request.method == 'POST':
  title = request.form.get('title')
  content = request.form.get('content')
  # データベースに保存
  post = Post(title=title, content=content)
  db.session.add(post)
  db.session.commit()
```

`request.form`にフォームのデータが入っているのでtitleとcontentを取得します
`post=Post(title=title, content=content)`で投稿のインスタンス(投稿データのPythonのオブジェクト)を作成します

```python
db.session.add(post)
db.session.commit()
```

データベースに投稿を加えて、commit（確定）します。

### データベースのデータを取り出す

```python
posts = Post.query.order_by(Post.created_at.desc()).all()
```

Postクラスからメソッドを指定してクラスに設定されているデータを取り出すことができます。(Postクラスなら投稿データ)


## FlaskでHTMLを扱う

### `render_template()`について

```Python
# python
# 投稿一覧を表示
return render_template('index.html', posts=posts)
```

`return render_template()`でHTMLを返します。関数の名前付き引数を指定することで指定した値をHTMLの中で使うことができます。`posts=posts`と指定することでHTMLの中で`posts`の内容を利用することができます。

```html
<!-- html -->
<h1>投稿一覧</h1>
<!-- postsから一つずつ要素を取り出す -->
{% for post in posts %}
    <div>
        <h2>{{ post.title }}</h2>
        <p>{{ post.content }}</p>
        <p>{{ post.created_at }}</p>
    </div>
{% endfor %}
```

HTMLの中でFlaskで使えるテンプレートエンジン(Jinja2テンプレート)に準拠してforやifを書くことができます。（標準のHTMLの書き方ではありません！）
これによってデータベースの内容に応じて動的にHTMLを生成することができます。

### `url_for()`について

```html
<!-- html -->
<a href="{{ url_for('create') }}">投稿作成</a>
```

`url_for()`はFlaskのルーティングの関数名からURLを生成するための関数です。
`url_for('index')`は`@app.route('/')`で定義した関数`index()`のURLを生成します。
`url_for('create')`は`@app.route('/create', methods=['GET', 'POST'])`で定義した関数`create()`のURLを生成します。

#### 活用方法

以下のようにHTMLのテンプレートを記述し、

```html
{% for post in posts %}
    <div>
        <h2>{{ post.title }}</h2>
        <p>{{ post.content }}</p>
        <p>{{ post.created_at }}</p>
    </div>
    <a href="{{url_for('edit',id=post.id)}}">編集</a>
    <a href="{{url_for('delete',id=post.id)}}">削除</a>
{% endfor %}
```

  データベースの内容がこのようになっているときHTMLは次のように出力されます
|id|title|content|created_at|
|-|-|-|-|
|1|今日は池袋の水族館に行きました|ペンギンがかわいかったです|2025-07-10|
|2|今日は大学に行きました|暑かった|2025-07-11|

```html
<div>
  <h2>今日は池袋の水族館に行きました</h2>
  <p>ペンギンがかわいかったです</p>
  <p>2025-07-10</p>
</div>
<a href="/edit/1">編集</a>
<a href="/delete/1">削除</a>
<div>
  <h2>今日は大学にに行きました</h2>
  <p>暑かったです</p>
  <p>2025-07-11</p>
</div>
<a href="/edit/2">編集</a>
<a href="/delete/2">削除</a>
```

投稿ごとに`title`、`content`、`created_at`、編集ページへのリンク、削除ページへのリンクを作成することができます。


### formについて

```html
<!-- html -->
<form action="{{ url_for('create') }}" method="post">
    <textarea type="text" name="title" placeholder="タイトル"></textarea>
    <textarea name="content" placeholder="内容"></textarea>
    <button type="submit">投稿</button>
</form>
```

formの中に文字を入力できる要素(input,textareaなど)を書いて`type='submit'`を指定したbuttonタグを設定するとデータを送信することができます。`<form action=`の後にデータを送信するURLを指定します。
`method="post"`はHTMLリクエストのmethod(リクエスト種類)にPOSTを指定します。methodには`GET`,`POST`,`PUT`,`DELETE`などありますが、基本的にGETとPOSTだけで問題ないでしょう。  