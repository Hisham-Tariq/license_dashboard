import subprocess
from flask import Flask, redirect, render_template, request, url_for
from os.path import exists
import socket
import os

app = Flask(__name__)

def read_key():
    if not exists('.license.silo'):
        return None
    else:
        # read the file and get the key
        key = ""
        with open('.license.silo', 'rb') as key_file:
            key = key_file.read()
        return key

def store_key(key):
    with open('.license.silo', 'wb') as key_file:
        key_file.write(key.encode())

def check_key_validation(key):
    result = subprocess.Popen(["/usr/bin/java", "-jar", "/var/www/license_dashboard/validator.jar", key], stdout=subprocess.PIPE).communicate()[0]
    return int(result)

def get_ip_address():
    result = subprocess.Popen(["/usr/bin/curl", "-4", "icanhazip.com"], stdout=subprocess.PIPE).communicate()[0]
    #s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    #s.connect(("8.8.8.8", 80))
    #return s.getsockname()[0];
    return result.decode("utf-8")

def stop_all_services():
    # os.system("/bin/systemctl stop wazuh-manager")
    os.system("/bin/systemctl stop kibana.service")
    # os.system("/bin/systemctl stop filebeat")
    # os.system("/bin/systemctl stop elasticsearch")

def start_all_services():
    # os.system("/bin/systemctl start wazuh-manager")
    os.system("/bin/systemctl start kibana.service")
    # os.system("/bin/systemctl start filebeat")
    # os.system("/bin/systemctl start elasticsearch")

@app.route("/activate", methods=['GET', 'POST'])
def activate_dashboard():
    if exists('.license.silo'):
        return redirect(url_for('redirect_to_dashboard'))
    stop_all_services()
    if request.method == 'POST':
        license_key = request.form['license_key']
        try:
            result = check_key_validation(license_key)
            if result == -1:
                stop_all_services()
                return render_template("activate.html", error="License key has expired")
            else:
                store_key(license_key)
                return redirect(url_for('redirect_to_dashboard'))
        except ValueError:
            stop_all_services()
            return render_template("activate.html", error="Invalid license key")
    return render_template("activate.html")

@app.route("/redirect")
def redirect_to_dashboard():
    key = read_key()
    if key is None:
        return redirect(url_for('activate_dashboard'))
    else:
        try:
            result = check_key_validation(key)
            if result == -1:
                stop_all_services()
                return redirect(url_for('activate_dashboard'))
            else:
                data = {"ip": get_ip_address(), "duration_left": result}
                start_all_services()
                return render_template("redirect.html", data = data)
        except ValueError:
            return render_template("activate.html", error="Invalid license key")


@app.route("/")
def index():
    if exists('.license.silo'):
        return redirect(url_for('redirect_to_dashboard'))
    else:
        return redirect(url_for('activate_dashboard'))

if __name__ == "__main__":
    stop_all_services()
    app.run(host='0.0.0.0')
