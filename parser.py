import csv

course_dict = {}
with open("/Users/amin/dons-hack-2023/HackCopy.csv", 'r') as file:
    csvreader = csv.reader(file)
    next(csvreader)
    for row in csvreader:
        valueList = []
        #This is meant to be the list that represents the name of the class[0]
        #The the days of the week that the class is offered[1]
        #and the the time[2]
        cur_course_number = row[1] + row[2] +  "-" + row[3]    # Getting the course name

        # To deal with empty rows
        if cur_course_number == "":
            cur_course_number = course_number
        else:
            course_number = cur_course_number

        #I made the value of the key to be a list where each index represents a different 
        #info

        valueList.append("Sec: " + row[3])
        valueList.append(row[6]) 
        valueList.append(row[7])
        valueList.append(row[8])


        course_dict[cur_course_number] = valueList



    # To get a specific course info, do:
    #print(course_dict['AEM120'][0])
    sorted_course_dict = dict(sorted(course_dict.items()))

    #print(sorted_course_dict)  # Uncomment this to see how the dictionary looks.

"""
Feel free to ask me anything
"""
#that returns a list of all possible schedules for a given list of class 

classId = "AEM124,ARCH350,BIOL105,BUS100"

    
#classId = input("Please enter your class Id: ")

def get_schedule(classId): 
    updatedDict = {}
    classIdList = classId.split(',')
    
    for course in classIdList:
        prefix = course.split('-')[0].lower()  # extract the course prefix and convert to lowercase
        if prefix not in [key.split('-')[0].lower() for key in course_dict.keys()]:
            print("No courses found for prefix:", prefix)
        else:
            for key in course_dict.keys():
                if key.lower().startswith(prefix):  # convert key to lowercase before checking
                    print(course_dict[key])
                    updatedDict[key] = course_dict[key]

    return updatedDict


selectedClass = get_schedule(classId)

#print(get_schedule(classId))

def checkConflict(selectedClass):

    return 0;





