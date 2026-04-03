import datetime
import os
import random
import re

from flask import Flask

app = Flask(__name__)
CARS = ["Chevrolet", "Renault", "Ford", "Lada"]
CATS = ["корниш-рекс", "русская голубая", "шотландская вислоухая", "мейн-кун", "манчкин"]

@app.route("/hello_world")
def hello_world():
    return "Привет, мир!"

@app.route("/cars")
def cars():
    return ", ".join(CARS)

@app.route("/cats")
def cats():
    random_cat = random.choice(CATS)
    return random_cat

@app.route("/get_time/now")
def get_time_now():
    current_time = datetime.datetime.now()
    return f"Точное время: {current_time}"

@app.route("/get_time/future")
def get_time_future():
    current_time_after_hour = datetime.datetime.now() + datetime.timedelta(hours=1)
    return f"Точное время через час будет {current_time_after_hour}"

def get_words_from_text(text):
    return re.findall(r"[A-Za-zА-Яа-яЁё-]+", text)

with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "war_and_peace.txt"), "r", encoding="utf-8") as book:
    book_text = book.read()
WORDS = get_words_from_text(book_text)

@app.route("/get_random_word")
def get_random_word():
    random_word = random.choice(WORDS)
    return random_word

@app.route("/counter")
def counter():
    counter.visits += 1
    return str(counter.visits)

counter.visits = 0

if __name__ == "__main__":
    app.run(debug=True)