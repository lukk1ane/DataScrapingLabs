students = {
    "Alice": 85,
    "Bob": 92,
    "Charlie": 78,
    "David": 90,
    "Eve": 88
}

def highest_scoring_student(students):
    return max(students, key=students.get)

def average_score(students):
    return sum(students.values()) / len(students)

def students_above_average(students):
    avg = average_score(students)
    return [name for name, score in students.items() if score > avg]

print("Highest Scoring Student:", highest_scoring_student(students))
print("Average Score:", average_score(students))
print("Students Above Average:", students_above_average(students))
