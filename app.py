from flask import Flask, render_template, request, abort
from nanoid import generate as nanoid
from database import database, migrate
import mimetypes
import os

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.sqlite3"
app.secret_key = os.urandom(256)

database.init_app(app)
migrate.init_app(app)


@app.get("/")
def index():
    return render_template("index.html")


@app.put("/files")
def upload_file():
    if not request.files or "file" not in request.files:
        return abort(400)

    file = request.files["file"]

    file_id = nanoid()
    extension = mimetypes.guess_extension(file.content_type)

    database[file_id] = f"/static/user_uploads/{file_id}{extension}"
    file.save(database[file_id][1:])

    return f"File was uploaded. {database[file_id]}"
