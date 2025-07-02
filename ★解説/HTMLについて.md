# FlaskでHTMLを扱う
## render_template()について

```Python
    # 投稿一覧を表示
    return render_template('index.html', posts=posts)
```

```return render_template()```でHTMLを返します。関数の名前付き引数を指定することで指定した値をHTMLの中で使うことができます

```html
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

## formについて

```html
<form action="{{ url_for('create') }}" method="post">
    <input type="text" name="title" placeholder="タイトル">
    <textarea name="content" placeholder="内容"></textarea>
    <button type="submit">投稿</button>
</form>
```

formの中に文字を入力できる要素(input,textareaなど)を書いて```type='submit'```を指定したbuttonタグを設定するとデータを送信することができます。```<form action=```の後にデータを送信するURLを指定します。
```{{ url_for('create') }}```はルーティングの関数名からURLを置き換えることができます。
```method="post"```はHTMLリクエストのmethod(リクエスト種類)にPOSTを指定します。methodにはGET,POST,PUT,DELETEなどありますが、基本的にGETとPOSTだけで問題ないでしょう。