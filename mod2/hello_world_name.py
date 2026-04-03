from datetime import datetime
from flask import Flask

app = Flask(__name__)

WEEKDAYS = (
    "понедельника",
    "вторника",
    "среды",
    "четверга",
    "пятницы",
    "субботы",
    "воскресенья",
)


@app.route("/hello-world/<name>")
def hello_world(name):
    weekday_index = datetime.today().weekday()
    weekday_name = WEEKDAYS[weekday_index]
    return f"Привет, {name}. Хорошей {weekday_name}!"
    

if __name__ == "__main__":
    app.run(debug=True)