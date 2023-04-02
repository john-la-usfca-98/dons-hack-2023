import scheduleParser
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)
@app.route("/", methods=('GET', 'POST'))
def fSchedule():
    schedules = ""
    if request.method == 'POST':
        inputs = request.form['classIds']
        res = scheduleParser.get_schedule(inputs)
        schedules = res[0]
        not_class = res[1]
        is_class = res[2]
        ranked = scheduleParser.rank_schedules(schedules, request.form['range'], request.form['time'])
        ranked = scheduleParser.print_rank_schedules(ranked)
        len_schedules = request.form['show_list']
        if len_schedules == "show_all":
            len_schedules = len(schedules)
        else:
            len_schedules = min(len(schedules), 5)
        #print(ranked)
        options = "Courses: " + request.form['classIds'] + ", Spread: " + request.form['range'] + ", Time: " + \
                  request.form['time']
        return render_template('schedule.html', schedules=ranked, options=options, len_schedules=len_schedules,
                               not_class=not_class, is_class=is_class)
    return render_template('schedule.html', schedules=schedules)

if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 5012, debug = True)
