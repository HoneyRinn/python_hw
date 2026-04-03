from flask import Flask

app = Flask(__name__)

storage = {}


@app.route("/add/<date>/<int:number>")
def add(date, number):
    year = int(date[:4])
    month = int(date[4:6])

    storage.setdefault(year, {}).setdefault(month, 0)
    storage[year][month] += number

    return f"Добавлено {number} рублей за {date}"


@app.route("/calculate/<int:year>")
def calculate_year(year):
    if year not in storage:
        return "0"

    total = sum(storage[year].values())
    return f"Суммарные траты за {year}: {total}"


@app.route("/calculate/<int:year>/<int:month>")
def calculate_month(year, month):
    if year not in storage or month not in storage[year]:
        return "0"

    return f"Суммарные траты за {year}-{month}: {storage[year][month]}"


if __name__ == "__main__":
    app.run(debug=True)