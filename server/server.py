from model import checkMessage, predict
from flask import Flask, request
from constants import ACTIONS

app=Flask(__name__)

@app.route("/health")
def health():
    return "boop"

@app.route("/check",methods=['GET'])
def check():
    pred = predict(request.args['msg'])
    print(pred)
    if pred >= ACTIONS['del'] :
        return "del"
    elif pred >= ACTIONS['warn'] :
        return "warn"
    return "pass"

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')