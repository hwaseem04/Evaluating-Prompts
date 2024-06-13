import re
import random
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, session
from openai import OpenAI
import time

app = Flask(__name__)
app.secret_key = "text123" # supposed to be taken from the environment variable. But for now, its okay.
db_path = './misc/DBs/principles.db'

client = OpenAI(api_key='sk-proj-tmR5ExbMdnZeFVs7OgH7T3BlbkFJLwrPmPTMiznz6IZJQBuA')

def get_all_rows():
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    rows = []
    for i in range(1, 27): #TODO: Change to full range
        table_name = f'principle{i}'
        c.execute(f'SELECT * FROM {table_name}')
        rows.extend(c.fetchall())
    conn.close()
    return rows

def generate_correctness(res1, res2):
    #TODO: Code to determine the most appropriate response
    return 1

def get_correctness(principle_id, questions_id):
    #TODO: Code to get the most appropriate response if present in the database already
    return 1

def create_chat_prompt(res1, res2):
    sys_msg = """Choose the better-written option. The first character of your response must be 1 for response 1 or 2 for response 2. After the first character, give a brief justification for your choice."""
    user_prompt = f"""Option 1: {res1}
                    Option 2: {res2} """
    
    return [
        {"role": "system", "content": sys_msg}, 
        {"role": "user", "content": user_prompt}
    ]

def get_openai_response(prompt):
    max_retries = 10
    attempt = 0
    while attempt < max_retries:
        try:
            response = client.chat.completions.create(messages=prompt,
                                                        model='gpt-4o')
            return response.choices[0].message.content
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            attempt += 1
            time.sleep(3)
    print(f"Failed to get chat completion after {max_retries} attempts")

def generate_preference(res1, res2): # TODO

    prompt = create_chat_prompt(res1, res2)
    res = get_openai_response(prompt)

    preference = int(res[0])
    justification = res[1:]
    return preference, justification

def get_preference(principle_id, questions_id):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    table_name = f'principle{principle_id}'
    c.execute(f"SELECT preference FROM {table_name} WHERE qid=?", (questions_id,))
    result = c.fetchone()
    conn.close()
    if result is None or result[0] == '':
        return None
    else:
        return int(result[0])

def save_preference(principle_id, questions_id, preference,):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    table_name = f'principle{principle_id}'
    print(type(preference), preference)
    c.execute(f"UPDATE {table_name} SET preference=? WHERE qid=?", (preference, questions_id))
    conn.commit()
    conn.close()

def decorate_text(text):
    text = text.replace('\n', '<br>')
    text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', text)
    # text = re.sub(r'### (.*?)(\n|$)', r'<h4>\1</h4>\2', text)
    return text

@app.route("/", methods=['POST', 'GET'])
def login():
    alert = False
    if 'index' not in session:
        session['index'] = 0
    
    rows = get_all_rows()
    
    if request.method == 'POST':
        if 'next' in request.form:
            session['index'] += 1
            if session['index'] >= len(rows):
                session['index'] = 0  # Reset to the first row if there are no more rows
            
            principle_id = rows[session['index']][0]   # Get the current principle_id
            questions_id = rows[session['index']][1]   # Get the current question_id
            existing_preference = get_preference(principle_id, questions_id)
            if existing_preference is not None:
                session['preference'] = int(existing_preference)
                session['justification'] = 'Loaded from database'
            elif 'preference' in session:
                del session['preference']
                del session['justification']
        
        elif 'prev' in request.form:
            session['index'] -= 1
            if session['index'] < 0:
                session['index'] = len(rows) - 1  # Go to the last row if the index goes below 0
            principle_id = rows[session['index']][0]   # Get the current principle_id
            questions_id = rows[session['index']][1]   # Get the current question_id
            existing_preference = get_preference(principle_id, questions_id)
            if existing_preference is not None:
                session['preference'] = int(existing_preference)
                session['justification'] = 'Loaded from database'
            elif 'preference' in session:
                del session['preference']
                del session['justification']
        
        elif 'getPref' in request.form:
            response1 = rows[session['index']][4]
            response2 = rows[session['index']][5]

            preference, justification = generate_preference( response1, response2)
            session['preference'] = preference
            session['justification'] = justification
        
        elif 'changePref' in request.form:
            principle_id = rows[session['index']][0]   # Get the current principle_id
            questions_id = rows[session['index']][1]   # Get the current question_id
            existing_preference = get_preference(principle_id, questions_id)
            # print('pref', existing_preference, type(existing_preference), 'qid :', questions_id)
            if existing_preference is not None:
                session['preference'] = 2 if existing_preference == 1 else 1
                session['justification'] = "Human Preference"
            elif 'preference' in session:
                session['preference'] = 2 if session['preference'] == 1 else 1
                session['justification'] = "Human Preference"
        
        elif 'getCorr' in request.form:
            response1 = rows[session['index']][4]
            response2 = rows[session['index']][5]
            correct_response_id = generate_correctness(response1, response2)

            #TODO
        
        elif 'changeCorr' in request.form:
            principle_id = rows[session['index']][0]   # Get the current principle_id
            questions_id = rows[session['index']][1]   # Get the current question_id
            existing_correctness = get_correctness(principle_id, questions_id)

            #TODO
        
        elif 'save' in request.form:
            if 'preference' in session:
                principle_id = rows[session['index']][0]  
                questions_id = rows[session['index']][1]  
                save_preference(principle_id, questions_id, session['preference'])
                print("saved")
                # del session['preference']
                # del session['justification']
                alert = True
    
    row = rows[session['index']] if rows else ('No data', 'No data', 'No data', 'No data')
    principle_id = row[0]
    questions_id = row[1]
    w_q = decorate_text(row[2])
    wo_q = decorate_text(row[3])
    w_r = decorate_text(row[4])
    wo_r = decorate_text(row[5])
    partition_texts = {
        'partition1': w_q,
        'partition2': wo_q,
        'partition3': w_r,
        'partition4': wo_r,
    }
    
    preference = session.get('preference', None)
    justification = session.get('justification', None)
    
    return render_template('index.html', partition_texts=partition_texts, index=session['index'], pid=principle_id, qid=questions_id, preference=preference, justification=justification, alert=alert)

if __name__ == "__main__":
    app.run(debug=True)
