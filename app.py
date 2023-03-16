from flask import Flask, render_template, request, abort, Response, redirect
from nanoid import generate as nanoid
from database import database, migrate, file_upload
from os.path import join, dirname, realpath
from configuration_parser import parse_configuration
from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler
import random
import os
import json

app = Flask(__name__)

app.config["UPLOAD_FOLDER"] = join(dirname(realpath(__file__)), "static/uploads")

parse_configuration(app)
app.secret_key = os.urandom(256)

database.init_app(app)
migrate.init_app(app)
file_upload.init_app(app, database)

from models.file import File


def clean_files_job():
    with app.app_context():
        files = File.query.all()

        for file in files:
            if datetime.now() > file.expires_in:
                try:
                    file = file_upload.delete_files(file, parent=True, files=["file"])

                    database.session.delete(file)
                    database.session.commit()

                    print(f"Deleted file {file.id}")
                except:
                    pass


scheduler = BackgroundScheduler()

scheduler.add_job(func=clean_files_job, trigger="interval", seconds=60)
scheduler.start()


@app.errorhandler(404)
def status_404_page(exception):
    return redirect("/")


@app.get("/")
def upload_page():
    return render_template("index.html",
                           extensions=app.config["ALLOWED_EXTENSIONS"],
                           upload_durations=enumerate(
                                app.config["UPLOAD_DURATIONS"]
                           ),
                           upload_durations_json=json.dumps(
                                app.config["UPLOAD_DURATIONS"]
                           ))


@app.put("/files")
def upload_file():
    if not request.files or \
        "file" not in request.files or \
            "upload_duration" not in request.form:
        return abort(400)

    uploaded_file = request.files["file"]
    upload_duration_index = int(
        request.form["upload_duration"]
    )

    if os.path.splitext(uploaded_file.filename)[-1][1:] \
        not in app.config["ALLOWED_EXTENSIONS"] or \
            upload_duration_index > len(app.config["UPLOAD_DURATIONS"]):
        return abort(400)

    upload_duration = app.config["UPLOAD_DURATIONS"][upload_duration_index]

    file_length = uploaded_file.seek(0, os.SEEK_END)
    if file_length / 1000000 > \
        upload_duration["maximum_file_size_in_mb"]:
        return abort(400)
    
    uploaded_file.seek(0, os.SEEK_SET)

    db_file = File(id=nanoid())

    db_file.content_type = uploaded_file.content_type
    db_file.expires_in = datetime.now() + timedelta(
        minutes=upload_duration["duration_in_minutes"]
    )
    db_file.password = random.choice(
        app.config["PASSWORDS"]
    )
    db_file.filename = uploaded_file.filename

    db_file.file_size = f"{(file_length / 1048576):.2f} мб"

    if file_length < 1024:
        db_file.file_size = f"{file_length} байт"
    elif file_length > 1024 and file_length < 1048576:
        db_file.file_size = f"{(file_length / 1024):.2f} кб"

    file_upload.add_files(db_file, files={"file": uploaded_file})

    database.session.add(db_file)
    database.session.commit()

    return render_template("upload-successful.html",
                           filename=db_file.filename,
                           file_size=db_file.file_size,
                           file_id=db_file.id,
                           password=db_file.password)


@app.get("/<file_id>")
def download_page(file_id):
    file = File.query.get_or_404(file_id)

    if datetime.now() > file.expires_in:
        file = file_upload.delete_files(file, parent=True, files=["file"])

        database.session.delete(file)
        database.session.commit()

        return abort(404)

    file_url = file_upload.get_file_url(file, filename="file")

    td = file.expires_in - datetime.now()
    days, hours, minutes = td.days, td.seconds // 3600, td.seconds % 3600 / 60.0

    expires_in = f"{int(minutes + (hours * 60) + (days * 60 * 24))} минут"

    return render_template("download.html", file=file, file_url=file_url, expires_in=expires_in)


@app.delete("/<file_id>/delete")
def delete_file(file_id):
    file = File.query.get_or_404(file_id)

    if file.password != request.form["password"]:
        return abort(400)

    file = file_upload.delete_files(file, parent=True, files=["file"])

    database.session.delete(file)
    database.session.commit()

    return Response(status=201, headers={"HX-Redirect": "/"})
