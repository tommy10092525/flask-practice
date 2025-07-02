# Flaskとデータベースを連携して、簡単なWebアプリを作ってみよう

- 必要なファイルを作成する
  - ```app.py```、```models.py```、```test.py```をつくる
  - ```templates```フォルダを作る
  - ```templates```フォルダの中に```create.html```と```index.html```を作る
- データベースを作成する
  - ```test.py```を実行する
  	- ```python test.py```で実行
  - ```instance/database.db```が作成されたことを確認する
- アプリケーションを起動する
  - ```python app.py```でアプリを起動してブラウザで確認する[リンク](http://127.0.0.1:5000/)。


**sqlalchemy**:データベースをPythonのオブジェクトとして定義する**ORM**のひとつ

### 説明

```app.py```アプリケーションの本体

```models.py```データベースのモデル定義

```db.py```データベースを作成する

## アプリケーションを起動する
```shell
python app.py
```

## データベースを作成する
```shell
python db.py
```
