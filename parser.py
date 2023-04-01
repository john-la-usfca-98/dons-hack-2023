import csv

course_dict = {}
with open("HackCopy.csv", 'r') as file:
    csvreader = csv.reader(file)
    next(csvreader)
    for row in csvreader:
        cur_course_number = row[1] + row[2]    # Getting the course name

        # To deal with empty rows
        if cur_course_number == "":
            cur_course_number = course_number
        else:
            course_number = cur_course_number

        """
        Format of the dictionary:
        - Key = Course number (Ex: AEM120, CS272)
        - Value = A list where:
            + First index = Course title
            + After: A string that looks like "Day: d, Time: time", where d is the day of the week (M,T,W,R,F)
            and time is the time 
        """
        for day in row[7]:
            """
            Some course titles have ',' in them so the parsing is kind of messed up. The next 2 lines of code
            is to remove those course entirely from the dictionary. You can comment them out to see the problem.
            The problematic course is UPA667
            """
            if day not in "MTWRF":
                continue

            if cur_course_number not in course_dict:
                course_dict[cur_course_number] = [row[6]]
            course_dict[cur_course_number] += ["Day: " + day + ", Time: " + row[8]]

print(course_dict) # Uncomment this to see how the dictionary looks. Ask me anything!!!