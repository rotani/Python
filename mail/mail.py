#!/usr/bin/env python
# -*- coding: utf-8 -*-
import configparser
import smtplib
import re
from os.path import expanduser
from email.mime.text import MIMEText
from email.header import Header
from email import charset

from email.mime.image import MIMEImage
from email.mime.audio import MIMEAudio
from email.mime.multipart import MIMEMultipart

class Mail():
  """
  メールを送信を行うクラス
  """
  def __init__(self, subject, body, sendto=None, sender=None, multiflag=False):
    """
    件名と本文をコンストラクタに与えるとメール送信を行ってくれる
    送信先と送信元を追加したバージョン
    """
    self._load()
    if sendto is not None:
      self.sendto  = sendto
    if sender is not None:
      inifile = self._getinifile()
      self.address = inifile.get(sender, "address")
      self.passwd  = inifile.get(sender, "passwd")
    self._send(subject, body, multiflag)

  def _send(self, subject, body, multiflag):
    con = smtplib.SMTP(self.smtpserver, self.smtpport)
    con.ehlo()
    con.login(self.address, self.passwd)
    cset ='utf-8'
    if multiflag:
      msg = body
    else:
      msg = MIMEText(body, 'plain', cset)
    msg['Subject'] = Header(subject, cset)
    msg['From'] = self.address
    # 現状、あて先は1人だけを想定している
    sendto = self.sendto.lstrip()
    m = re.search("(.+) <(.+@.+)>", sendto)
    if m:
      msg['To'] = "%s <%s>" % (Header(m.groups()[0], cset), m.groups()[1])
    else:
      msg['To'] = sendto
    con.sendmail(self.address, [self.sendto], msg.as_string())
    con.close()
    
  def _load(self):
    """
    configファイルを読み込んでメールの設定を行う
    """
    inifile = self._getinifile()
    self.address = inifile.get("mail", "address")
    self.passwd = inifile.get("mail", "passwd")
    self.sendto = inifile.get("mail", "sendto")
    self.smtpserver = inifile.get("mail", "smtpserver")
    self.smtpport = inifile.get("mail", "smtpport")

  def _getinifile(self):
    home = expanduser("~")
    inifile = configparser.SafeConfigParser()
    confpath = home + "/.config.ini"
    inifile.read(confpath)
    return inifile

def attachImage(subject, body, sendto=None, path=None, fname=None):
  '''
  画像添付メール
  '''
  # マルチパートメールの本文は呼び出し側で設定する
  msg  = MIMEMultipart()
  body = MIMEText(body, 'plain', 'utf-8')
  msg.attach(body)

  # 画像データの読み込み
  try:
    with open(path, "rb") as fp:
      img = MIMEImage(fp.read(), fname.split('.')[-1], name=fname)
      msg.attach(img)
      m = Mail(subject, msg, sendto, multiflag=True)
  except Exception as e:
    print("画像データ読み込みエラー発生:%s" % e)

def attachAudio(subject, body, sendto=None, path=None, fname=None, subtype=None):
  '''
  音声ファイルの添付
  '''
  # マルチパートメールの本文は呼び出し側で設定する
  msg  = MIMEMultipart()
  body = MIMEText(body, 'plain', 'utf-8')
  msg.attach(body)

  # 音声データの読み込み
  try:
    with open(path, "rb") as fp:
      img = MIMEAudio(fp.read(), _subtype=subtype, Name=fname)
      msg.attach(img)
      m = Mail(subject, msg, sendto, multiflag=True)
  except Exception as e:
    print("音声データ読み込みエラー発生:%s" % e)
  

def htmlMail(subject, body, sendto=None, path=None, fname=None):
  '''
  GmailにHTMLファイルを送信する
  HTMLにはsrc要素でリンクsrcを指定したものを用意する
  '''
  import base64
  msg  = MIMEMultipart()
  
  # 画像データの読み込み
  try:
    with open(path, "rb") as f:
      img = MIMEImage(f.read(), fname.split('.')[-1], name=fname)
      img.add_header('Content-ID', '<' + fname + '>')
      msg.attach(img)

    # 'iso-2022-jp'でエンコード
    body = body.encode('iso-2022-jp')
    body = MIMEText(body, 'html', _charset="ISO-2022-JP")
    msg.attach(body)
    Mail(subject, msg, sendto, multiflag=True)
  except Exception as e:
    print("画像埋め込みメール作成でエラー発生:%s" % e)
  
