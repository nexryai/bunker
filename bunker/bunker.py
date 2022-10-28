import os
import sys
import boto3
import gnupg
import yaml
import subprocess
import datetime

class print_message:
    def info(self, message):
        sys.stdout.write("\033[32m ✔ \033[0m " + str(message) + "\n")

    def error(self, message):
        sys.stdout.write("\033[31m ✗ \033[0m " + str(message) + "\n")

    def fetal_error(self, message, e):
        exception = str(e)
        sys.stderr.write("\033[31m" + "=!=========FETAL ERROR=========!=" + "\n")
        sys.stderr.write(str(message) + "\n")
        sys.stderr.write("Exception >>> " + exception+ "\n")
        sys.stderr.write("================================="+ "\033[0m\n")


def main():
    msg = print_message()
    msg.info("Starting bunker backup...")

    # 設定ファイルを開く
    try:
        with open('/etc/bunker/config.yml', 'r') as yml:
            config = yaml.safe_load(yml)
    except FileNotFoundError as e:
        msg.fetal_error("Config file does not exist.", e)
    except Exception as e:
        msg.fetal_error("Faild to load /etc/bunker/config.yml", e)
        sys.exit (1)

    # 必須の設定項目を読み込み
    try:
        server_name = config['server_name']
        s3_endpoint = config['s3_endpoint']
        s3_access_key = config['s3_access_key']
        s3_secret_access_key = config['s3_secret_access_key']
        s3_bucket_name = config['s3_bucket_name']
        backup_dirs = config['backup_dirs']
    except TypeError as e:
        msg.fetal_error("Config file is invalid.", e)
        sys.exit(1)
    except Exception as e:
        msg.fetal_error("An error occurred while loading the config file.", e)
        sys.exit(1)

    # 設定任意の項目を読み込み
    try:
        pre_backup_exec = config['pre_backup_exec']
    except TypeError as e:
        msg.info("pre_backup_exec is undefined")
    
    try:
        encrypt_keys = config['encrypt_keys']
    except TypeError as e:
        msg.info("encrypt_keys is undefined")

    try:
        post_backup_exec = config['post_backup_exec']
    except TypeError as e:
        msg.info("post_backup_exec is undefined")

    # gnupgのディレクトリ検出
    home_dir = os.environ['HOME']

    try:
        gnupg_dir = os.environ['BUNKER_GNUPG_DIR']
    except KeyError:
        gnupg_dir = home_dir + "/.gnupg"

    if os.path.exists(gnupg_dir) == False:
        msg.error("Faild to detect gnupg dir ! \n Please set BUNKER_GNUPG_DIR environment variable.")
        sys.exit (1)

    # pre_backup_exec
    for pre_command in pre_backup_exec:
        cmd_args = pre_command.split()
        try:
            subprocess.check_output(cmd_args)
        except Exception as e:
            msg.fetal_error(f"pre_backup_exec command ({pre_command}) did not complete successfully.", e)
            sys.exit(1)
        else:
            msg.info(f"pre_backup_exec command ({pre_command}) executed successfully!")

    # バックアップするディレクトリが存在するか
    for chk_dir in backup_dirs:
        if os.path.exists(chk_dir) == False:
            msg.error(f"backup directory ({chk_dir}) does not exist")
            sys.exit (1)
    
    # 圧縮
    backup_dirs_list = []
    for dir_name in backup_dirs:
        backup_dirs_list.append(dir_name)

    msg.info("Backup dirs: " + str(backup_dirs_list))

    try:
        tar_command = ['tar', 'acf', 'l0'] + backup_dirs_list
        subprocess.check_output(tar_command)
    except Exception as e:
        msg.fetal_error("tar command did not complete successfully.", e)
        sys.exit(1)
    else:
        msg.info("Successfully compressed the backup directory!")

    # 暗号化
    gpg = gnupg.GPG(gnupghome=gnupg_dir)
    enc_layer = 0

    for use_key in encrypt_keys:
        try:
            with open(f'l{str(enc_layer)}', 'rb') as f:
                enc_layer += 1
                msg.info(f"Layer:{enc_layer}  Encrypt file with PGP key ({use_key})...")
                gpg.encrypt_file(f, recipients=use_key, output=f"l{str(enc_layer)}")
        except Exception as e:
            msg.fetal_error("Failed to encrypt file.", e)
            sys.exit(1)
        else:
            os.remove(f'l{enc_layer - 1}')

    date = datetime.datetime.now()
    backup_filename = f"{date.strftime('%Y-%m-%d_%H-%M-%S')}.backup"
    os.rename(f"l{enc_layer}", backup_filename) 

    # ファイルアップロード
    s3 = boto3.resource('s3',
        endpoint_url = s3_endpoint,
        aws_access_key_id = s3_access_key,
        aws_secret_access_key = s3_secret_access_key
    )

    bucket = s3.Bucket(s3_bucket_name)

    msg.info("Uploading files...")
    #bucket.upload_file(backup_filename, f"{server_name}/{backup_filename}")
    msg.info("Success!")

    # post_backup_exec
    for post_command in post_backup_exec:
        cmd_args = post_command.split()
        try:
            subprocess.check_output(cmd_args)
        except Exception as e:
            msg.fetal_error(f"pre_backup_exec command ({post_command}) did not complete successfully.", e)
            sys.exit(1)
        else:
            msg.info(f"pre_backup_exec command ({post_command}) executed successfully!")



if __name__ == '__main__':
    main()