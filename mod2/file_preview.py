import os
from flask import Flask, abort

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


@app.route("/preview/<int:size>/<path:relative_path>")
def preview(size, relative_path):
    file_path = os.path.abspath(os.path.join(BASE_DIR, relative_path))

    if not os.path.isfile(file_path):
        abort(404)

    with open(file_path, "r", encoding="utf-8") as file:
        result_text = file.read(size)

    result_size = len(result_text)
    return f"<b>{file_path}</b> {result_size}<br>{result_text}"


if __name__ == "__main__":
    app.run(debug=True)