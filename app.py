from flask import Flask, render_template, request, session, redirect
import random

app = Flask(__name__)
app.secret_key = 'any_secret_key'

TOTAL_QUESTIONS = 5

def generate_question():
    num1 = random.randint(1, 10)
    num2 = random.randint(1, 10)
    operator = random.choice(['+', '-', '*', '/'])

    if operator == '+':
        answer = num1 + num2
    elif operator == '-':
        answer = num1 - num2
    elif operator == '*':
        answer = num1 * num2
    elif operator == '/':
        num2 = random.randint(1, 10)
        answer = round(num1 / num2, 2)

    question = f"What is {num1} {operator} {num2}?"
    return question, answer

@app.route("/", methods=["GET", "POST"])
def home():
    if 'current_question' not in session:
        session['score'] = 0
        session['current_question'] = 0
        question, answer = generate_question()
        session['question'] = question
        session['answer'] = answer
    elif request.method == "POST":
        try:
            player_answer = float(request.form["answer"])
            correct_answer = session.get('answer')
            if player_answer == correct_answer:
                session['score'] += 1
        except ValueError:
            return render_template("index.html", question=session['question'], score=session['score'], message="Enter a valid number!")

        session['current_question'] += 1
        if session['current_question'] >= TOTAL_QUESTIONS:
            score = session['score']
            session.clear()
            return render_template("game_over.html", score=score, total_questions=TOTAL_QUESTIONS)
        else:
            question, answer = generate_question()
            session['question'] = question
            session['answer'] = answer

    return render_template("index.html", question=session['question'], score=session['score'])

if __name__ == "__main__":
    app.run(debug=True)
