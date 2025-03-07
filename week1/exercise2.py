import random


def read_file_stats(file_path):
    with open(file_path, "r") as file:
        return eval(file.read())


def generate_student_names(data):
    words = data.get("words", 10)
    return [f"Student_{i}" for i in range(1, words + 1)]


def find_highest_scoring_student(students):
    return max(students, key=students.get)


def compute_average_score(students):
    return sum(students.values()) / len(students) if students else 0


def students_above_average(students, average):
    return {name: score for name, score in students.items() if score > average}


extracted_data = read_file_stats("file_stats.txt")
student_names = generate_student_names(extracted_data)
students = {name: random.randint(50, 100) for name in student_names}

highest_student = find_highest_scoring_student(students)
average_score = compute_average_score(students)
above_avg_students = students_above_average(students, average_score)

print(
    f"Highest Scoring Student: {highest_student} with {students[highest_student]} points"
)
print(f"Average Score: {average_score:.2f}")
print(f"Students Above Average: {above_avg_students}")
