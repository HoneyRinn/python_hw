from flask import Flask, request
from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, TextAreaField
from wtforms.validators import Email, InputRequired, NumberRange
from wtforms.validators import ValidationError
import subprocess
from flask import request

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret-key"


@app.route("/ps")
def ps():
    args = request.args.getlist("arg")

    if args:
        command = ["ps", "".join(args)]
    else:
        command = ["ps"]

    result = subprocess.run(
        command,
        capture_output=True,
        text=True,
        check=False,
    )

    output = result.stdout if result.stdout else result.stderr
    return f"<pre>{output.strip()}</pre>"


def get_system_uptime() -> str:
    result = subprocess.run(
        ["uptime", "-p"],
        capture_output=True,
        text=True,
        check=False,
    )

    uptime_text = (result.stdout or result.stderr).strip()

    if uptime_text.startswith("up "):
        uptime_text = uptime_text[3:]

    return uptime_text


@app.route("/uptime")
def uptime():
    uptime_value = get_system_uptime()
    return f"Current uptime is {uptime_value}"


def number_length(min: int, max: int, message: str | None = None):
    def _number_length(form, field):
        if field.data is None:
            return

        value = abs(field.data)
        digits_count = len(str(value))

        if field.data <= 0 or digits_count < min or digits_count > max:
            raise ValidationError(
                message or f"Число должно содержать от {min} до {max} цифр"
            )

    return _number_length


class NumberLength:
    def __init__(self, min: int, max: int, message: str | None = None):
        self.min = min
        self.max = max
        self.message = message

    def __call__(self, form, field):
        if field.data is None:
            return

        value = abs(field.data)
        digits_count = len(str(value))

        if field.data <= 0 or digits_count < self.min or digits_count > self.max:
            raise ValidationError(
                self.message or f"Число должно содержать от {self.min} до {self.max} цифр"
            )


class RegistrationForm(FlaskForm):
    email = StringField(
        "email",
        validators=[
            InputRequired(message="Поле email обязательно"),
            Email(message="Некорректный email"),
        ],
    )
    phone = IntegerField(
        "phone",
        validators=[
            InputRequired(message="Поле phone обязательно"),
            number_length(10, 10, message="phone должен содержать 10 цифр и быть положительным"),
        ],
    )
    name = StringField(
        "name",
        validators=[InputRequired(message="Поле name обязательно")],
    )
    address = StringField(
        "address",
        validators=[InputRequired(message="Поле address обязательно")],
    )
    index = IntegerField(
        "index",
        validators=[InputRequired(message="Поле index обязательно")],
    )
    comment = TextAreaField("comment")


@app.route("/registration", methods=["GET", "POST"])
def registration():
    form = RegistrationForm()

    if form.validate_on_submit():
        return "OK"

    if request.method == "POST":
        return {"errors": form.errors}, 400

    return "Registration form"


if __name__ == "__main__":
    app.run(debug=True)