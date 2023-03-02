from database import database, file_upload


@file_upload.Model
class File(database.Model):
    __tablename__ = "files"

    id = database.Column(database.String(255), primary_key=True)
    content_type = database.Column(database.String(255), nullable=False)
    expires_in = database.Column(database.DateTime())
    password = database.Column(database.String(255))
    filename = database.Column(database.String(255))
    file_size = database.Column(database.String(255))
    file = file_upload.Column()
