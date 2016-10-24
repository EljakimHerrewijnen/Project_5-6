import time
from flask import Flask
print("HELLLOOOO")
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

if __name__ == "__main__":
    app.run()
time.sleep(20)