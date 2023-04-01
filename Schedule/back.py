import parser
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)
@app.route("/")
@app.route("/home")

def fSchedule():
    return render_template('schedule.html')

if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 5000, debug = True)