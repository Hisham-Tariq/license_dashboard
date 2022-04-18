from ipaddress import ip_address
from flask import Flask, redirect, render_template, url_for
from os.path import exists
import socket
from cryptography.fernet import Fernet

app = Flask(__name__)


licenses = [
    {
        "hash": "kajhdankdsjgkjheqrfnmkiuenfmf",
        "duration": "1d",
    },
    {
        "hash": "sdkfjdskjowrjolwemngkjrwjmsdf",
        "duration": "7d",
    },
    {
        "hash": "dkjjuyerjjhvhjiukjwejhkouywewe",
        "duration": "14d",
    },
    {
        "hash": "ksdfazsxdcfvghbnjkmjhfdhnjkhgj",
        "duration": "1M",
    }

];


@app.route("/activate")
def activate_dashboard():
    return render_template("activate.html")

@app.route("/redirect")
def redirect_to_dashboard():
    return render_template("redirect.html")


def intialize_licenses_file():
    if not exists('.key.silo'):
        # key generation
        key = Fernet.generate_key()
        # string the key in a file
        with open('encryption.key', 'wb') as filekey:
            filekey.write(key)
        
    with open('filekey.key', 'rb') as filekey:
        key = filekey.read()
        fernet = Fernet(key)
        with open('.licnenses.silo', 'wb') as licenses:
            licenses.write(fernet.encrypt(licenses))


@app.route("/")
def index():
    intialize_licenses_file();
    if exists('.license_keys.silo'):
        return redirect(url_for('redirect_to_dashboard'))
    else:
        return redirect(url_for('activate_dashboard'))

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip_address = s.getsockname()[0];
    return redirect(url_for('activate_dashboard'))

if __name__ == "__main__":
    app.run(host='0.0.0.0')

