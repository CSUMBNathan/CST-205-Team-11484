from flask_bootstrap import Bootstrap5
from flask import Flask, render_template
import random

app = Flask(__name__)
bootstrap = Bootstrap5(app)

urls = ['https://www.youtube.com/watch?v=dQw4w9WgXcQ',
'https://www.youtube.com/watch?v=Bf7NOcO8kTs']

@app.route('/')
def home():
   return render_template('home.html')

@app.route('/guess')
def guess():
    return render_template('guess.html')

@app.route('/guessed')
def guessed():
    return render_template('guessed.html')

@app.route('/add_link')
def add_link():
    return render_template('add_link.html')