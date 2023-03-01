from database import database, file_upload


@file_upload.Model
class File(database.Model):
    __tablename__ = "files"

    id = database.Column(database.String(255), primary_key=True)
    content_type = database.Column(database.String(255), nullable=False)
    file = file_upload.Column()
