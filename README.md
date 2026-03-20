# LINE Messaging APIサンプルプログラム
- Messaging APIを使ってLINEにごみ捨ての通知をします。2022年から使用しているものを外部向けに書き直したものです
- サンプルとは言いつつも私が常用しているものがベースです。私の住んでいる自治体に合わせた曜日設定になっているので、適宜ご自分の住居に合わせた設定にしてください
- LINEが利用しているPydantic V1互換レイヤーがPython 3.14で警告を出すので気になる方は**Python 3.13**以下で実行してください。

## 必要パッケージのインストール
```bash
python install -r requirements.txt
```

## Messaging APIの設定
このプログラムにはLINEのMessaging APIから2つの情報を取得する必要があります。
1. LINE_CHANNEL_ACCESS_TOKEN : LINEの特定の「会話」にメッセージを流すためのトークン
2. LINE_USER_ID : あなたのID
入力がなかった場合はエラーを出力して終了します

### 情報はどこにあるか
[LINE Developersのコンソール](https://developers.line.biz/console/)にログインする。
1. LINE_CHANNEL_ACCESS_TOKEN 
専用に作ったチャネル→Messaging API設定→チャンネルアクセストークン
2. LINE_USER_ID
専用に作ったチャネル→チャネル基本設定→あなたのユーザーID

.env.sampleを.envに変更して「チャンネルアクセストークン」「ユーザーID」を上記に置き換えてください。
この程度の規模であればハードコードしても良いかも知れませんが、その辺りはお任せします


### 曜日の設定
```python
if weekday == 3:  # 木曜の夜
    send_message("[ゴミ捨て通知]明日は資源ゴミの日です。Powered By GCP")
elif weekday in (2, 6):  # 水曜と日曜の夜
    send_message("[ゴミ捨て通知]明日は燃えるゴミの日です。Powered By GCP")
elif weekday == 0 and (8 <= day <= 14 or 22 <= day <= 28):  # 月曜の夜
    send_message("[ゴミ捨て通知]明日は燃えないゴミの日です。Powered By GCP")
```
上記のweekdayで曜日の設定をしています。(0=月, 1=火, 2=水, 3=木, 4=金, 5=土, 6=日)
ごみ捨ての**前日**にお知らせをするものなので…
- 金曜日の朝に資源ごみ　→　木曜日の夜にお知らせ
- 月曜日と木曜日に燃えるごみ　→　日曜日と水曜日の夜にお知らせ

という設定です。燃えないゴミは第2,4火曜日のみなので「8-14日と22-28日の範囲に該当する水曜日が第2と第4」という条件になります。

### 通知時刻
```python
schedule.every().day.at("21:00").do(schedule_message)
```
毎晩21時にschedule_messageを実行しますが、先述の設定に含まれない曜日では何も行われません。

## 実行
```bash
python garbage_notifier.py
```
正しく設定されていれば、決まった時刻にLINEのｷﾝｺｰﾝでお知らせしてくれることでしょう。
あとはsystemd等で自動起動してくれるように設定すればマシンを再起動したときも安心です。