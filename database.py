from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_file_upload.file_upload import FileUpload

database = SQLAlchemy()
migrate = Migrate(db=database)
file_upload = FileUpload(db=database)
