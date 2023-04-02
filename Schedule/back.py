import scheduleParser
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)
@app.route("/", methods=('GET', 'POST'))
def fSchedule():
    schedules = ""
    if request.method == 'POST':
        inputs = request.form['classIds']
        schedules = scheduleParser.get_schedule(inputs)
        ranked = scheduleParser.rank_schedules(schedules, request.form['range'], request.form['time'])
        ranked = scheduleParser.print_rank_schedules(ranked)
        print(ranked)
        options = "Courses: " + request.form['classIds'] + ", Spread: " + request.form['range'] + ", Time: " + request.form['time']
        return render_template('schedule.html', schedules=ranked, options=options)
    return render_template('schedule.html', schedules=schedules)

if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 5012, debug = True)
