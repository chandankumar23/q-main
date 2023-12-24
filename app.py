from flask import Flask, render_template, request, redirect, url_for, session, json, jsonify
import sqlite3

app = Flask(__name__)
app.secret_key = 'supersecretkey'


conn = sqlite3.connect('user_choices.db')
cursor = conn.cursor()

users = {'john': 'password', 'jane': '12345'}
subjects_list = ['Biology']
user_choices = {}
with open('question_biology.json', 'r') as file:
    questions_data = json.load(file)


def number_to_alphabet(number):
    # Convert a number to the corresponding alphabet (A, B, C, ...)
    return chr(ord('A') + number - 1)


# def read_json_file():
#     try:
#         with open(JSON_FILE_PATH, 'r') as file:
#             data = json.load(file)
#     except FileNotFoundError:
#         data = {}
#     return data

# def write_json_file(data):
#     with open(JSON_FILE_PATH, 'w') as file:
#         json.dump(data, file)




@app.route('/')
def hello_world():
    return "<p>Hello, World!</p>"

@app.route('/home')
def home_page():
    return "<p>Welcome to Home Page!</p>"

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username] == password:
            session['username'] = username
            return redirect(url_for('dashboard'))
            # return redirect(url_for(practice_papers(username)))
        return render_template('login.html', error='Invalid username or password')
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        username = session['username']
        # with open('questions.json') as file:
        #     question_list = json.load(file)
        return render_template('dashboard.html', username=username, practice_papers=subjects_list)
    return redirect(url_for('login'))


# @app.route('/practice-papers/question/<int:question_id>')
# def display_question(question_id):
#         # paper = questions_data[category]
#         question_id =1
#         question = next((q for q in questions_data if q['question_id'] == question_id), None)
#         return render_template('question.html', question=question,question_id = question_id)




@app.route('/question/<int:question_id>')
def display_question(question_id):
        question = next((q for q in questions_data if q['question_id'] == question_id), None)
        return render_template('question.html', question=question)


@app.route('/save_choice/<int:question_id>', methods=['POST'])
def save_choice(question_id):
    choice = request.form.get('choice')

    alphabet_choice = number_to_alphabet(int(choice))


    # Save the user's choice
    # user_choices[question_id] = choice

    user_choices[question_id] = {'question_id': question_id, 'choice': alphabet_choice}

    # Write the user's choices to a user_choices.json file
    with open('user_choices.json', 'w') as json_file:
        json.dump(list(user_choices.values()), json_file, indent=2)

    # Calculate the next question ID
    next_question_id = question_id + 1

    # If there is a next question, redirect to it; otherwise, display a completion message
    # if next_question_id <= 100:

    if next_question_id <= len(questions_data):
        return redirect(url_for('display_question', question_id=next_question_id))
    else:
        return 'Assignment completed! Thank you!'
    


@app.route('/review/<int:question_id>', methods=['GET'])
def review_page(question_id):
    question = next((q for q in questions_data if q['question_id'] == question_id), None)
    return render_template('review.html', question=question)

    # question_id = questions_data['question_id']
    # if 0 <= question_id < len(questions_data):
    #     question = questions_data[question_id]
    #     return render_template('review.html', question=question, index=question_id, total=len(questions_data))
    # else:
    #     return "Question not found!"

# # @app.route('/review', methods=['GET','POST'])
# # def review():
# #     if 'username' in session:
# #         # return render_template('review.html',username=username, questions=questions[test], selected_answers=selected_answers.get(test, {}))
# #         return render_template('review.html')

# #     return redirect(url_for('login'))

# # @app.route("/editprofile")
# # def edit_profile():
# #     return render_template("index.html", title="Second page")

if __name__ == '__main__':
    app.run(debug=True)
