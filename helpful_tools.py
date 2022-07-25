import os

def clear():
    os.system('cls' if os.name == 'nt' else '')

def get_question(question_id, a_list):
    return (list(filter(lambda question: question['id']==question_id, a_list)))
    

def check_answer(answer, real):
    lena = len(answer.split())
    lenr = len(real.split())
    a = 0
    r = 0
    for word in answer.lower().split():
        if word in real.lower():
            a += 1
    if a == lena:
        return True
    for word in real.lower().split():
        if word in answer.lower():
            r += 1
    if r == lenr:
        return True
    return False
    