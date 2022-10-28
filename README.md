# bunker
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg?style=for-the-badge)](https://opensource.org/licenses/Apache-2.0)
[![Repo](https://img.shields.io/badge/nexryai%2Fbunker-master-lightgrey?style=for-the-badge&logo=gitlab)](https://git.sda1.net/nexryai/bunker)
[![python](https://img.shields.io/badge/python-EEE?style=for-the-badge&logo=python)](https://www.python.org/)
<br><br>
安全にオブジェクトストレージにディレクトリをバックアップする小さくてスマートなPythonプログラム  
 - バックアップするファイルはアップロードする前にGPGを使用して複数の層で暗号化できます。あなた以外にファイルが読まれる心配はありません。エンドツーエンド暗号化を実現します。
 - pipを使用してインストール可能。様々な環境で使えます。
 - バックアップ前後に任意のコマンドを実行可能。サーバーのバックアップにも最適です。

## インストール
`pip install git+https://git.sda1.net/nexryai/bunker`

## 設定
### Step1
PGP鍵を生成します。複数レイヤーで暗号化したい場合は複数生成します。この作業はサーバー以外のマシンで行うことを推奨します。  
生成した鍵のIDを覚えておきます。

### Step2
`gpg --export-keys --armor [生成した鍵のID] > public.key`で公開鍵をエクスポートし、サーバへ送りつけます。テキストファイルとして開けるのでサーバーにsshで繋ぎエディターに貼っつけるのがおすすめです。  
送りつけたら`gpg --import [ファイル名]`でインポートします。

### Step
`/etc/bunker/config.yml` を作成し以下のように設定を行います。

```
server_name: server1

# S3 Object storage config
s3_endpoint: https://<accountid>.r2.cloudflarestorage.com
s3_access_key: <access_key>
s3_secret_access_key: <access_key_secret>
s3_bucket_name: <bucket_name>

# backup config

# Number of backups to keep
save_backups: 5

backup_dirs:
  - /path/to/backup/dir
  
pre_backup_exec:
  - command_1

encrypt_keys:
  - <gpg_key_id_1>
  - <gpg_key_id_2>
  
post_backup_exec:
  - command_2
```


## 使い方
### バックアップ
`bunker backup` をrootとして実行するだけです。

###リストア
秘密鍵を生成したマシンで `bunker restore` を実行します。
