student_scores = {
    "Alice": 85,
    "Bob": 92,
    "Charlie": 78,
    "David": 88,
    "Eve": 95
}

def find_highest_scoring_student(scores):
    highest_student = max(scores, key=scores.get)
    return highest_student, scores[highest_student]

def compute_average_score(scores):
    total_score = sum(scores.values())
    average_score = total_score / len(scores)
    return average_score

def get_students_above_average(scores):
    average_score = compute_average_score(scores)
    above_average_students = [name for name, score in scores.items() if score > average_score]
    return above_average_students

if __name__ == "__main__":
    highest_student, highest_score = find_highest_scoring_student(student_scores)
    average_score = compute_average_score(student_scores)
    above_average_students = get_students_above_average(student_scores)

    print(f"Highest Scoring Student: {highest_student} with a score of {highest_score}")
    print(f"Average Score: {average_score:.2f}")
    print("Students Above Average:", above_average_students)