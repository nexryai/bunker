# bunker
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg?style=for-the-badge)](https://opensource.org/licenses/Apache-2.0)
[![Repo](https://img.shields.io/badge/nexryai%2Fbunker-master-lightgrey?style=for-the-badge&logo=gitlab)](https://git.sda1.net/nexryai/bunker)
[![python](https://img.shields.io/badge/python-EEE?style=for-the-badge&logo=python)](https://www.python.org/)
<br><br>
安全にオブジェクトストレージにディレクトリをバックアップする小さくてスマートなPythonプログラム

## インストール
`pip install git+https://git.sda1.net/nexryai/bunker`

## 設定
`/etc/bunker/config.yml`  
```
server_name: server1

# S3 Object storage config
s3_endpoint: https://<accountid>.r2.cloudflarestorage.com
s3_access_key: <access_key>
s3_secret_access_key: <access_key_secret>
s3_bucket_name: <bucket_name>

# backup config
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
