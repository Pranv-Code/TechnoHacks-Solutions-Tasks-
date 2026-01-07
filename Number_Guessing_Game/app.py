from flask import Flask, redirect, request, session, render_template, url_for,flash
import random

app = Flask(__name__)
app.secret_key = "SECRET_GAME"
START_LIMIT = 1
END_LIMIT = 10
CHANCES = 5
@app.route('/')
def landing():
    return render_template('home.html')

@app.route('/start', methods=["POST","GET"])
def start_game():
    player_name = request.form.get('player_name')

    session['user'] = player_name
    session['count'] = 0
    session['num'] = random.randint(START_LIMIT, END_LIMIT)
    session['chances'] = 0

    return render_template('game.html')

@app.route('/guess', methods=["POST","GET"])
def guess_number():
    if session.get('count', 0) >= CHANCES - 1:
        return redirect(url_for('result', res='failed'))

    guessed_number = int(request.form.get('guessed_number'))

    if guessed_number == session['num']:
        return redirect(url_for('result', res='success'))
    else:
        session['count'] += 1
        session['chances'] = CHANCES - session['count']
        msg = hint(guessed_number)
        # We pass the message here. In CSS, we will make 'alert-info' red.
        return render_template('game.html', message=f"WRONG GUESS! : {msg}")

def hint(guessed_number):
    if guessed_number > session['num']:
        return f'Try Smaller Than {guessed_number}'
    else:
        return f'Try Grater Than {guessed_number}'

@app.route('/result/<res>')
def result(res):
    if res == 'failed':
        session.clear()

    return render_template('result.html', result=res)
