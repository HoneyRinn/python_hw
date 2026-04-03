from flask import Flask, abort

app = Flask(__name__)


@app.route("/max_number/<path:numbers>")
def max_number(numbers):
    parts = numbers.split("/")

    try:
        numbers_list = [int(part) for part in parts]
    except ValueError:
        return "Переданы не все числа", 400

    max_value = max(numbers_list)
    return f"Максимальное переданное число <i>{max_value}</i>"


if __name__ == "__main__":
    app.run(debug=True)