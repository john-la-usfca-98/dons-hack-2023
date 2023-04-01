import csv
from itertools import combinations
from datetime import datetime
import itertools
import sys

def parse_time(t):
    try:
        return datetime.strptime(t, '%I:%M %p').time()
    except ValueError:
        return datetime.strptime(t, '%I:%M%p').time()

course_dict = {}
with open("HackCopy.csv", 'r') as file:
    csvreader = csv.reader(file)
    next(csvreader)
    for row in csvreader:
        valueList = []

        cur_course_number = row[1] + row[2] +  "-" + row[3]

        if cur_course_number == "":
            cur_course_number = course_number
        else:
            course_number = cur_course_number
        valueList.append("CRN: " + row[0])
        valueList.append("Sec: " + row[3])
        valueList.append(row[7])
        if '-' in row[8]:
            start_time, end_time = row[8].split('-')
            valueList.append(start_time.strip())
            valueList.append(end_time.strip())
        else:
            valueList.append(row[8].strip())
            valueList.append('')  # Add an empty string for end_time if it's not available

        valueList.append(row[18])
        #Instructor name^
        course_dict[cur_course_number] = valueList

argu = sys.argv[1]
classId = sys.argv[1]

def check_conflict(class1, class2):
    days1 = set(class1[1])
    days2 = set(class2[1])

    start_time1 = parse_time(class1[3])
    end_time1 = parse_time(class1[4])
    start_time2 = parse_time(class2[3])
    end_time2 = parse_time(class2[4])

    if days1.intersection(days2) and (start_time1 < end_time2 and start_time2 < end_time1):
        return True
    return False

def get_schedule(classId): 
    class_sections = {}
    classIdList = classId.split(',')
    
    for course in classIdList:
        prefix = course.split('-')[0].lower()
        if prefix not in [key.split('-')[0].lower() for key in course_dict.keys()]:
            print("No courses found for prefix:", prefix)
        else:
            class_sections[prefix] = []
            for key in course_dict.keys():
                if key.lower().startswith(prefix):
                    class_sections[prefix].append(key)

    possible_schedules = []

    for section_combinations in itertools.product(*class_sections.values()):
        conflict = False

        for i, class1 in enumerate(section_combinations[:-1]):
            if conflict:
                break
            for class2 in section_combinations[i + 1:]:
                if check_conflict(course_dict[class1], course_dict[class2]):
                    conflict = True
                    break

        if not conflict:
            possible_schedules.append(section_combinations)

    return possible_schedules

# Add the following functions to compute the ranking score based on user preferences
def compute_spread_score(schedule):
    days = set()
    for course in schedule:
        days.update(set(course_dict[course][2]))
    return len(days)

def compute_time_preference_score(schedule, time_preference):
    total_score = 0
    for course in schedule:
        if time_preference == "early":
            total_score -= parse_time(course_dict[course][3]).hour
        elif time_preference == "late":
            total_score += parse_time(course_dict[course][3]).hour
    return total_score

def rank_schedules(schedules, spread_preference, time_preference):
    ranked_schedules = sorted(
        schedules,
        key=lambda schedule: (
            compute_spread_score(schedule) if spread_preference == "spread" else -compute_spread_score(schedule),
            compute_time_preference_score(schedule, time_preference),
        ),
        reverse=True
    )
    return ranked_schedules

# Get the schedules
schedules = get_schedule(classId)

if len(schedules) == 0:
    print("There are no possible schedules.")
    sys.exit()

# After getting the schedules, ask for user preferences
spread_preference = input("Do you want your courses spread out through the week or bunched up together? (spread/bunch): ").lower()
while spread_preference not in ("spread", "bunch"):
    spread_preference = input("Invalid input. Please enter 'spread' or 'bunch': ").lower()

time_preference = input("Do you prefer classes earlier or later in the day? (early/late): ").lower()
while time_preference not in ("early", "late"):
    time_preference = input("Invalid input. Please enter 'early' or 'late': ").lower()

# Rank the schedules based on user preferences
ranked_schedules = rank_schedules(schedules, spread_preference, time_preference)

# Display the top 5 ranked schedules
print("\nTop 5 schedules based on your preferences:")
for i, schedule in enumerate(ranked_schedules[:5]):
    print(f"Rank {i+1}:")
    for course in schedule:
        course_info = course_dict[course]
        print(f"{course_info[0]} {course}: {course_info[1]}, {course_info[2]}, {course_info[3]}-{course_info[4]} {course_info[5]}")
    print("\n")

# Give the user the choice to display all schedule combinations
show_all = input("Do you want to see all the schedule combinations? (yes/no): ").lower()
while show_all not in ("yes", "no"):
    show_all = input("Invalid input. Please enter 'yes' or 'no': ").lower()

if show_all == "yes":
    print("\nAll schedule combinations:")
    for i, schedule in enumerate(ranked_schedules):
        print(f"Schedule {i+1}:")
        for course in schedule:
            course_info = course_dict[course]
            print(f"{course_info[0]} {course}: {course_info[1]}, {course_info[2]}, {course_info[3]}-{course_info[4]} {course_info[5]}")
        print("\n")

