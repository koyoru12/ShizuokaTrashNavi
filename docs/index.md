# エンドポイントの構成
エンドポイントはLINEのWebhookとするものと、アプリケーション本体の処理を行うものとで分かれる。
LINEエンドポイントはLINEとのインターフェースとして振る舞い
アプリエンドポイントはインターフェースに関係なく処理を行う。

## /api/app/message
ユーザの発話イベントを受け付け、応答メッセージを返却する。

### メソッド
POST

### 認証
必要(外部からはアクセス不能)

### リクエスト

|param|type|required|desc|
|:--|:--|:--|:--|
|user_id|string|true|LINEのユーザID|
|request_message|string|true|ユーザが入力した文字列|
|client|string|true|'line'または'web'|
|config|object|false|コンフィグオブジェクト|
|action|string|false|アクション文字列|

```
{
    user_id: '0123abcd',
    request_message: 'ペットボトル'
}
```

#### config

|param|type|required|desc|
|:--|:--|:--|:--|
|search_city|string|false|検索市町村の指定|

search_cityが指定された場合、ユーザに紐付けられている市町村情報より優先される。

#### action

ポストバックアクションとして使われる。
基本的にはサーバが発行したaction文字列をそのまま返却すれば良く
その内容についてクライアントが関知する必要はない。
中身はurlに用いられるクエリ形式(a=1&b=2)の文字列。
actionパラメータが指定されている場合、他のあらゆるレスポンス処理に優先して処理される。

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

## /api/app/address
ユーザの位置情報設定イベントを受け付け、応答メッセージを返却する。
ユーザがごみ分別情報を検索する市町村を設定する。

### メソッド
POST

### 認証
必要(外部からはアクセス不能)

### リクエスト
|param|type|required|desc|
|:--|:--|:--|:--|
|user_id|string|true|LINEのユーザID|
|longitude|float|true|経度|
|latitude|float|true|緯度|

### レスポンス
※/api/app/messageと同じ


## /api/app/city
botで検索可能な市町村の一覧を返却する。

### メソッド
GET

### 認証
不要

### リクエスト
※パラメータなし


# メッセージオブジェクト
メッセージオブジェクトにはbotからの応答メッセージが格納されている。
メッセージオブジェクトは、type属性によって識別され、その他の属性は各メッセージごとに異なる。
メッセージのtype属性は以下のとおり。

|type|desc|note|
|:--|:--|:--|
|help|ユーザからのヘルプメッセージに対する応答||
|thanks|'ありがとう'など好意的なメッセージに対する応答||
|mistake|'違う'などネガティブなメッセージに対する応答||
|require_address|まだ位置情報が登録されていないユーザに位置情報を求めるメッセージ|LINEのみ|
|trash_info|ごみの検索がなされた際の応答/見つからなかった場合の応答も含まれる||
|trash_select|ごみの検索でヒット数が多い際にユーザに選択を求める応答||
|response_address_success|位置情報の登録に成功した場合の応答|LINEのみ|
|response_address_reject|位置情報の登録に失敗した(市町村が登録されていない)場合の応答|LINEのみ|
|help_search_trash|ごみの検索の仕方に対するヘルプ応答||

# データベース
データベースはSQLiteを使用する。

## trash.db
ごみ情報に関するデータベース。

### trashテーブル
個々のごみ情報を格納するテーブル。
市町村関係なくすべてこのテーブルに格納する。

|key|column|desc|
|:--|:--|:--|
|○|id|プライマリキー|
||city_id|cityテーブルのid|
||name|ごみの名称(ex.ペットボトル)|
||category|ごみの分類(ex.燃えるゴミ)|
||note|備考|

### cityテーブル
市町村情報を格納するテーブル。
trashテーブルにひとつでも登録のある市町村が登録される。

|key|column|desc|
|:--|:--|:--|
|○|id|プライマリキー|
||pref_name|県名(静岡のみ)|
||city_name|市町村名(ex.静岡市)|

### synonymテーブル
類語テーブル。
検索のヒット率をあげるため日本語Wordnetから引用してきている。
効果がいまいち分からないので将来的に見直しするかもしれない。

|key|column|desc|
|:--|:--|:--|
|○|id|プライマリキー|
||name|類語名|

### trash_synonymテーブル
trashテーブルとsynonymテーブルを対応させるテーブル。

|key|column|desc|
|:--|:--|:--|
||trash_id|trashテーブルのid|
||synonym_id|synonymテーブルのid|


### fixedreplyテーブル
固定応答メッセージを格納するテーブル。
ユーザの発話をmatchカラムでLIKE検索を行い、マッチしたら応答する。
実際の応答内容はテーブルには格納されず、メッセージオブジェクトを生成する段階で指定される。

|key|column|desc|
|:--|:--|:--|
|○|id|プライマリキー|
||message_type|メッセージオブジェクトのtype属性(ex.help)|
||match|マッチする語句(ex.ヘルプ%)|

