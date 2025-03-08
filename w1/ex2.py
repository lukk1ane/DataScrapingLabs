from ex1 import score_data


def generate_students(content):
    st = []

    name = None
    score = None
    for word in content['words']['content']:
        if word.isdigit():
            score = word
        elif word.istitle():
            name = word

        if name is not None and score is not None:
            st.append({
                'name': name,
                'score': int(score)
            })
            name = score = None
    return st


students = generate_students(score_data)


def highest_scoring_student(studs):
    return max(studs,key=lambda x : x['score'])

def score_average(studs):
    return sum([s['score'] for s in studs])/len(studs)

def above_average(studs):
    average = score_average(studs)
    return list(filter(lambda x : x['score'] > average, studs))

print(f'students: {students}\n')
print(f'highest scoring student: {highest_scoring_student(students)}\n')
print(f'score average: {score_average(students)}\n')
print(f'above average students: {above_average(students)}\n')