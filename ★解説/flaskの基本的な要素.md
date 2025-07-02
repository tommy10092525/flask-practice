```python
from flask import Flask
app = Flask(__name__)
@app.route('/')
def index():
    return "Hello world!"

if __name__ == '__main__':
    app.run(debug=True)
```
このように書いて実行するとWebサーバーが立ち上がり、URLのアクセスに対してレスポンスを返すことができます
```@app.route('/')```の@はデコレータと呼びます。（難しいから書き方だけ覚えればＯＫ！）


