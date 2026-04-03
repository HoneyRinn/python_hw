import shutil
import subprocess
import sys
import traceback

from flask import Flask, jsonify
from flask_wtf import FlaskForm
from wtforms import IntegerField, TextAreaField
from wtforms.validators import InputRequired, NumberRange

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret-key"
app.config["WTF_CSRF_ENABLED"] = False


class Redirect:
    def __init__(self, *, stdout=None, stderr=None):
        self.new_stdout = stdout
        self.new_stderr = stderr
        self.old_stdout = None
        self.old_stderr = None

    def __enter__(self):
        self.old_stdout = sys.stdout
        self.old_stderr = sys.stderr

        if self.new_stdout:
            sys.stdout = self.new_stdout
        if self.new_stderr:
            sys.stderr = self.new_stderr

        return self

    def __exit__(self, exc_type, exc_value, tb):
        if exc_type is not None and self.new_stderr:
            sys.stderr.write(traceback.format_exc())
            
        sys.stdout = self.old_stdout
        sys.stderr = self.old_stderr
        return False


class BlockErrors:
    def __init__(self, error_types: set[type[BaseException]]):
        self.error_types = error_types

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is None:
            return False  # ничего не произошло

        # если ошибка подходит — гасим её
        if any(issubclass(exc_type, err) for err in self.error_types):
            return True

        # иначе пробрасываем дальше
        return False


class CodeForm(FlaskForm):
    code = TextAreaField(
        "code",
        validators=[InputRequired(message="Поле code обязательно")],
    )
    timeout = IntegerField(
        "timeout",
        validators=[
            InputRequired(message="Поле timeout обязательно"),
            NumberRange(min=1, max=30, message="timeout должен быть от 1 до 30"),
        ],
    )


def run_code(code: str, timeout: int) -> tuple[str, str, bool]:
    if shutil.which("prlimit"):
        command = ["prlimit", "--nproc=1:1", sys.executable, "-c", code]
    else:
        command = [sys.executable, "-c", code]

    process = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )

    try:
        stdout, stderr = process.communicate(timeout=timeout)
        return stdout, stderr, False
    except subprocess.TimeoutExpired:
        process.kill()
        stdout, stderr = process.communicate()
        return stdout, stderr, True


@app.route("/run_code", methods=["POST"])
def run_user_code():
    form = CodeForm()

    if not form.validate_on_submit():
        return jsonify({"errors": form.errors}), 400

    stdout, stderr, timed_out = run_code(form.code.data, form.timeout.data)

    if timed_out:
        return "Время выполнения кода истекло", 408

    result = (stdout or "") + (stderr or "")
    return result.strip() if result.strip() else ""
    

if __name__ == "__main__":
    app.run(debug=True)