import scheduleParser
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)
@app.route("/", methods=('GET', 'POST'))
def fSchedule():
    schedules = ""
    if request.method == 'POST':
        inputs = request.form['classIds']
        schedules = scheduleParser.get_schedule(inputs)
        ranked = scheduleParser.rank_schedules(schedules, "bunch", "late")
        ranked = scheduleParser.print_rank_schedules(ranked)
        print(ranked)
        return render_template('schedule.html', schedules=ranked)
    return render_template('schedule.html', schedules=schedules)

if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 5011, debug = True)
