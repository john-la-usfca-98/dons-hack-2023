import scheduleParser
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)
"""
Compiles data for the "\" page (Home page).
Renders the schedule.html file in the templates folder
"""
@app.route("/", methods=('GET', 'POST'))
def fSchedule():
    schedules = ""

    # Change the page when a POST request is received ("Generate Schedule" button clicked)
    if request.method == 'POST':
        inputs = request.form['classIds']   # Getting the class IDs from the user input

        # Process to get the ranked schedules
        res = scheduleParser.get_schedule(inputs)
        schedules = res[0]
        not_class = res[1]  # Invalid inputs
        is_class = res[2]   # Valid inputs
        ranked = scheduleParser.rank_schedules(schedules, request.form['range'], request.form['time'])
        ranked = scheduleParser.print_rank_schedules(ranked)
        len_schedules = request.form['show_list']   # Option to show how many schedules

        # Deciding the number of schedules to be printed out
        if len_schedules == "show_all":
            len_schedules = len(schedules)
        else:
            len_schedules = min(len(schedules), 5)

        # Getting data for the event calendar
        schedule_list = []
        for i in range(len_schedules):
            possible_schedule_dict = {}
            for schedule in ranked[i]:
                info = schedule.split(',')
                course_num = info[0].split(" ")[2]
                days = info[1].replace(" ", "")
                time = info[2][:18]
                for day in days:
                    if day not in possible_schedule_dict:
                        possible_schedule_dict[day] = []
                    possible_schedule_dict[day].append(course_num)
            schedule_list.append(possible_schedule_dict)
        #print(schedule_list)

        # Printing out the selected options for easier debugging
        options = "Courses: " + request.form['classIds'] + ", Spread: " + request.form['range'] + ", Time: " + \
                  request.form['time']

        # Re-rendering the template to show the schedules
        return render_template('schedule.html', schedules=ranked, options=options, len_schedules=len_schedules,
                               not_class=not_class, is_class=is_class, schedule_list=schedule_list)

    return render_template('schedule.html', schedules=schedules)

if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 5016, debug = True)
