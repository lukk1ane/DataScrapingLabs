from Week1.Exercise1 import FileProcessor


class StudentRecords:
    def __init__(self, file_stats):
        self.students = self._generate_sample_students(file_stats)

    def _generate_sample_students(self, file_stats):
        if not file_stats:
            return {}
        return {f"Student{i + 1}": (file_stats['words'] + i * 10) % 100 for i in range(file_stats['lines'])}

    def find_highest_scorer(self):
        return max(self.students.items(), key=lambda x: x[1]) if self.students else None

    def compute_average_score(self):
        return sum(self.students.values()) / len(self.students) if self.students else 0

    def get_students_above_average(self):
        avg = self.compute_average_score()
        return {name: score for name, score in self.students.items() if score > avg}


# usage
file_processor = FileProcessor("data.txt")
if file_processor.data:
    print(file_processor.data)
    student_records = StudentRecords(file_processor.data)
    print("Students:", student_records.students)
    print("Highest Scorer:", student_records.find_highest_scorer())
    print("Average Score:", student_records.compute_average_score())
    print("Students Above Average:", student_records.get_students_above_average())
