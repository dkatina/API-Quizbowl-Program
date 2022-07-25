
import requests
import json
import base64
from random import choice

url = 'https://cae-bootstore.herokuapp.com'

endpoint_login = "/login"
endpoint_user = "/user"
endpoint_question = "/question"      #can add /all to get all questions, can also add /<id> to get specific questions

def register_user(payload):
    if payload['email'] == 'dylankatina@gmail.com':
        payload['admin'] = True
    payload_json_string = json.dumps(payload)
    headers = {
        'Content-Type':'application/json'
    }
    response = requests.post(
        url + endpoint_user,
        data = payload_json_string,
        headers = headers
    )
    return response.text

def login_user(user_name, password):
    auth_string = user_name + ":" + password
    
    headers={
        'Authorization' : "Basic "+base64.b64encode(auth_string.encode()).decode()
    }
    user_data = requests.get(
        url + endpoint_login,
        headers=headers
    )
    return user_data.json()

def get_all_admin_questions(token): 
    headers = {"Authorization": "Bearer "+token}
    questions = requests.get(
        url+endpoint_question,
        headers=headers)
    return questions.json()['questions']

def get_all_questions(token):
    headers = {"Authorization": "Bearer "+token}
    questions = requests.get(
        url+endpoint_question+'/all',
        headers=headers)
    return questions.json()['questions']

def get_quiz(token):
    headers = {"Authorization": "Bearer "+token}
    questions = requests.get(
        url+endpoint_question+'/all',
        headers=headers)
    quiz = []
    n = 0
    while n < 10:
        q = choice(questions.json()['questions'])
        if q not in quiz:
            quiz.append(q)
            n += 1 
    return quiz

def create_a_question(token, payload):
    payload_json_string = json.dumps(payload)
    headers={
        'Content-Type':'application/json',
        'Authorization':'Bearer ' + token
    }
    response = requests.post(
        url+endpoint_question,
        data=payload_json_string,
        headers=headers
    )
    return response.text

def edit_specific_question(token, payload, id):
    payload_json_string = json.dumps(payload)
    headers={
        'Content-Type':'application/json',
        'Authorization':'Bearer ' + token
    }
    response = requests.put(
        url+endpoint_question+'/'+str(id),
        data=payload_json_string,
        headers=headers
    )
    return response.text

def delete_question(token, id):
    headers = {"Authorization": "Bearer "+token}
    response = requests.delete(
        url+endpoint_question+'/'+str(id),
        headers=headers
    )
    return response.text

