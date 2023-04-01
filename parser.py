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

        #print("Days: " + row[7] + " Time: " + row[8])

        course_dict[cur_course_number] = ["Days: " + row[7] + " Time: " + row[8]]
print(course_dict)