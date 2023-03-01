from flask import Flask, render_template, request, abort
from nanoid import generate as nanoid
from database import database, migrate, file_upload
from os.path import join, dirname, realpath
import mimetypes
import os

app = Flask(__name__)

app.config["UPLOAD_FOLDER"] = join(dirname(realpath(__file__)), "static/uploads")

app.config["ALLOWED_EXTENSIONS"] = ["jpg", "png", "mov", "mp4", "mpg"]
app.config["MAX_CONTENT_LENGTH"] = 1000 * 1024 * 1024

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.sqlite3"

app.secret_key = os.urandom(256)

database.init_app(app)
migrate.init_app(app)
file_upload.init_app(app, database)

from models.file import File


@app.get("/")
def index():
    return render_template("index.html")


@app.put("/files")
def upload_file():
    if not request.files or "file" not in request.files:
        return abort(400)

    uploaded_file = request.files["file"]

    db_file = File(id=nanoid())
    db_file.content_type = uploaded_file.content_type

    file_upload.add_files(db_file, files={"file": uploaded_file})

    database.session.add(db_file)
    database.session.commit()

    return f"File was uploaded. {file_upload.get_file_url(db_file, filename='file')}"
