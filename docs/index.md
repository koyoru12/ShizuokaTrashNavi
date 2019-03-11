# エンドポイントの構成
エンドポイントはLINEのWebhookとするものと、アプリケーション本体の処理を行うものとで分かれる。
LINEエンドポイントはLINEとのインターフェースとして振る舞い
アプリエンドポイントはインターフェースに関係なく処理を行う。

## /app/message
ユーザの発話イベントを受け付け、応答メッセージを返却する。

### リクエスト
|param|type|desc|
|:--|:--|:--|
|user_id|string|LINEのユーザID|
|request_message|string|ユーザが入力した文字列|

```
{
    user_id: '0123abcd',
    request_message: 'ペットボトル'
}
```

### レスポンス
|param|type|desc|
|:--|:--|:--|
|messages|messageの配列||

```
{
    messages: [
        {},
        {},
        ...
    ]
}
```

## /app/address
ユーザの位置情報設定イベントを受け付け、応答メッセージを返却する。
ユーザがごみ分別情報を検索する市町村を設定する。

### リクエスト
|param|type|desc|
|:--|:--|:--|
|user_id|string|LINEのユーザID|
|longitude|float|経度|
|latitude|float|緯度|

### レスポンス
※/app/messageと同じ

# メッセージオブジェクト
