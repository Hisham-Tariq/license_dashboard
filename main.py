from flask import Flask
app = Flask(__name__)

@app.route("/")
def index():
    return "<a href='https://192.168.100.131:442' style='color:red'>Kibana Dashboard!</a>"

if __name__ == "__main__":
    app.run(host='0.0.0.0')

