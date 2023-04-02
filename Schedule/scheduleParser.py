import csv
import requests
from io import StringIO
from itertools import combinations
from datetime import datetime
import itertools
import sys


def parse_time(t):
    try:
        return datetime.strptime(t, '%I:%M %p').time()
    except ValueError:
        return datetime.strptime(t, '%I:%M%p').time()


profRating = {}

file_path = 'rateProf.csv'

# Getting data for the professor ratings dictionary
with open(file_path, mode='r', newline='') as csvfile:
    csvreader = csv.reader(csvfile)

    # Reading the rows (data)
    for row in csvreader:
        temp = []
        temp = row[0].split(';')
        name_parts = temp[1].split()
        first_name = name_parts[0]
        last_name = name_parts[-1]
        key = (first_name[:2] + last_name).lower()
        profRating[key] = temp[0]


url = "https://drive.google.com/file/d/1VBgk_-EiNG3idVckxQpzzKedVYlqQGVH/view?usp=share_link"

# Convert the Google Drive link to a direct download link
file_id = url.split("/")[5]
dwn_url = "https://drive.google.com/uc?id=" + file_id

# Download the CSV file content
response = requests.get(dwn_url)
response.raise_for_status()

# Read the CSV file content
csv_data = StringIO(response.text)
csvreader = csv.reader(csv_data)
next(csvreader)

# Getting data for the course dictionary
course_dict = {}
#with open("HackCopy.csv", 'r') as file:
    #csvreader = csv.reader(file)
    #next(csvreader)
for row in csvreader:
    valueList = []

    cur_course_number = row[1] + row[2] + "-" + row[3]

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
    # Instructor name^
    course_dict[cur_course_number] = valueList

#argu = sys.argv[1]
#classId = sys.argv[1]
"""
Checks the schedule between 2 course to see if there are any conflicts
@:return: True if there is a conflict, False otherwise
"""
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

"""
Generates a list of possible schedules from the given list of class IDs
@:param classId: The list of class IDs
@:return: A list of possible schedules, valid inputs and invalid inputs according to their times
"""
def get_schedule(classId):
    classId = classId.replace(" ", "")
    class_sections = {}
    classIdList = classId.split(',')
    res = []
    not_class = []
    is_class = []

    # Looking through the list of class IDs to see valid course numbers
    for course in classIdList:
        prefix = course.split('-')[0].lower()
        if prefix not in [key.split('-')[0].lower() for key in course_dict.keys()]:
            print("No courses found for prefix:", prefix)
            not_class += [prefix]
        else:
            is_class += [prefix.upper()]
            class_sections[prefix] = []
            for key in course_dict.keys():
                if key.lower().startswith(prefix):
                    class_sections[prefix].append(key)

    # Generating the possible schedules
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

    # Appending to the result
    res.append(possible_schedules)
    res.append(not_class)
    res.append(is_class)
    return res


"""
Computes the time score for the schedules for ranking
@:param schedules: The schedule to compute score for 
@:param spread_preference: Bunched up or Spreaded out classes
@:return: The total score of a schedule
"""
def compute_spread_score(schedule):
    days = set()
    for course in schedule:
        days.update(set(course_dict[course][2]))
    return len(days)

"""
Computes the time score for the schedules for ranking
@:param schedules: The schedule to compute score for 
@:param time_preference: Early or Late classes
@:return: The total score of a schedule
"""
def compute_time_preference_score(schedule, time_preference):
    total_score = 0
    for course in schedule:
        if time_preference == "early":
            total_score -= parse_time(course_dict[course][3]).hour
        elif time_preference == "late":
            total_score += parse_time(course_dict[course][3]).hour
    return total_score

"""
Ranks the possible schedules according to the user's preferences
@:param schedules: The list of schedules to be ranked
@:param spread_preference: Bunch or Spread out schedules
@:param time_preference: Early or Late classes
@:return: A ranked schedules
"""
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

"""
Gets a professor's rating from the profRating dictionary
@:param professor_name: the name of the professor to look for
@:return: The rating if it exists or NR otherwise
"""
def get_professor_rating(professor_name):
    name_parts = professor_name.split()
    first_name = name_parts[0]
    last_name = None

    for part in reversed(name_parts):
        if part.startswith("("):
            continue
        else:
            last_name = part
            break

    key = (first_name[:2] + last_name).lower()

    for prof_key, rating in profRating.items():
        if prof_key.lower() == key:
            return rating

    return "NR"



# Get the schedules
# schedules = get_schedule(classId)
"""
if len(schedules) == 0:
    print("There are no possible schedules.")
    sys.exit()
"""

# After getting the schedules, ask for user preferences
"""
spread_preference = input("Do you want your courses spread out through the week or bunched up together? (spread/bunch): ").lower()
while spread_preference not in ("spread", "bunch"):
    spread_preference = input("Invalid input. Please enter 'spread' or 'bunch': ").lower()

time_preference = input("Do you prefer classes earlier or later in the day? (early/late): ").lower()
while time_preference not in ("early", "late"):
    time_preference = input("Invalid input. Please enter 'early' or 'late': ").lower()

# Rank the schedules based on user preferences
ranked_schedules = rank_schedules(schedules, spread_preference, time_preference)
"""

"""
Display the top 5 ranked schedules
@:param ranked_schedules: the list of ranked schedules
@:return a list of strings representing the ranked schedules
"""
def print_rank_schedules(ranked_schedules):
    res = []
    for i, schedule in enumerate(ranked_schedules):
        temp = []
        for course in schedule:
            course_info = course_dict[course]
            prof_rating = get_professor_rating(course_info[5])
            temp += [course_info[0] + " " + course + ", " + course_info[2] + ", " + course_info[
                3] + "-" + course_info[4] + " " + course_info[5] + ", RMP Rating: " + prof_rating]
        res.append(temp)
    return res


"""
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
"""
