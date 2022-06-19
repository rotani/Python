# Pythonスクリプトから画像埋め込みメール送信

emailモジュールを使ってメール送信する際の作成したモジュールの使い方メモ

## 使い方

### 1. tar.gzからのpip install mymail-x.y.z.tar.gz
### 2. ホームディレクトリに.config.iniファイルの設定

  以下の内容を自身の環境に合わせて記載する。
  ```
  # -*- coding: utf-8 -*-
  [mail]
  address    = 送信元アドレス
  passwd     = 送信元アドレスに対するパスワード
  sendto     = デフォルトの宛先
  smtpserver = SMTPサーバ
  smtpport   = SMTPサーバのポート番号
  ```

### 3. 単純なメール送信

  件名(subject)と本文(body)を設定し、オブジェクト生成することでメール送信が完了する。

  この時の宛先は、config.iniファイルに記載したsendto宛に送信する。

  他には、sendto=None, sender=None, multiflag=False などが設定可能。
  
  ```
  from mail import Mail
  subject = 'メールのテスト'
  body    = 'メールの本文'
  m = Mail(subject, body)
  ```

### 4. 画像添付メール

   ```
   from mail import attachImage
   #  m = Mail('メールのテスト', 'メールのテスト')

   subject = '添付メールのテスト'
   body    = '添付画像の前に表示するメッセージ内容'
   path    = 画像ファイルのパス(フルパス)
   fname   = 画像ファイルの名前(添付画像ファイルの名前となる)

   attachImage(subject, body, path=path, fname=fname)
   ```

### 5. 音声ファイルの添付

   ```
   from mail import attachAudio

   subject = '音声ファイル添付のテスト'
   body    = '本文のメッセージ内容'
   path    = 音声ファイルのパス(フルパス)
   fname   = 音声ファイルの名前(添付ファイルの名前となる)
   subtype = 'audio/mpeg'(参考リンク先のよくあるMIMEタイプを参照)

   attachAudio(subject, body, path=path, fname=fname, subtype=subtype)
   ```

### 6. 画像埋め込みメール送信

   画像埋め込み時のimg要素のsrc属性を"cid:"+ファイル名(fname)にすることで参照が可能となる。

   ```
   from mail import htmlMail
   subject = '画像埋め込みメールのテスト'
   path    = 画像ファイルのパス(フルパス)
   fname   = 画像ファイルの名前
   body    = '''
   <div>
    <img src="cid:%s" alt="添付ファイルを参照(PNG)">
    </div>
   ''' % fname

   htmlMail(subject, body, path=path, fname=fname)
   ```

## 制約事項

送信先のアドレスに複数アドレスを設定することは想定していない

## 参考
[email.mime: メールと MIME オブジェクトを一から作成 — Python 3.10.0b2 ドキュメント](https://docs.python.org/ja/3/library/email.mime.html)

[よくある MIME タイプ - HTTP | MDN](https://developer.mozilla.org/ja/docs/Web/HTTP/Basics_of_HTTP/MIME_types/Common_types)
