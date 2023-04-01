from flask import Flask, render_template, request, jsonify

app = Flask(__name__)
@app.route("/", methods=('GET', 'POST'))
def fSchedule():
    schedules = ""
    if request.method == 'POST':
        schedules = request.form['classIds']
        return render_template('schedule.html', schedules=schedules)
    return render_template('schedule.html', schedules=schedules)

if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 5011, debug = True)
