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

        schedule_list = []
        for i in range(len_schedules):
            possible_schedule_dict = {}
            for schedule in ranked[i]:
                info = schedule.split(',')
                course_num = info[0].split(" ")[2][:-1]
                days = info[1].replace(" ", "")
                time = info[2][:18]
                for day in days:
                    if day not in possible_schedule_dict:
                        possible_schedule_dict[day] = []
                    possible_schedule_dict[day].append(course_num)
            schedule_list.append(possible_schedule_dict)
        print(schedule_list)

        options = "Courses: " + request.form['classIds'] + ", Spread: " + request.form['range'] + ", Time: " + \
                  request.form['time']
        return render_template('schedule.html', schedules=ranked, options=options, len_schedules=len_schedules,
                               not_class=not_class, is_class=is_class, schedule_list=schedule_list)
    return render_template('schedule.html', schedules=schedules)

if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 5013, debug = True)
