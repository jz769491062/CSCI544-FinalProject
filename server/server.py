from model import checkMessage
from flask import Flask, request

app=Flask(__name__)

@app.route("/health")
def health():
    return "boop"

@app.route("/check",methods=['GET'])
def check():
    return checkMessage(request.args['msg'])

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')