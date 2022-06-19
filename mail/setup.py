# -*- coding: utf-8 -*-
from setuptools import setup

setup(
  name         = 'mymail', # 配布ファイルを指定。モジュールにちなんだ配布ファイルの名前をつけるのが一般的
  version      = '0.0.1',
  description  = 'emailモジュールを使ってメール送信する際の備忘録',
  author       = 'Ryo Otani',
  author_email = 'ryo.otani@gmail.com',
  url          = 'https://github.com/rotani',
  py_modules   = ['mymail'], # パッケージに入れる.pyファイルのリスト。
)
