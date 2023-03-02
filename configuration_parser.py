import json


def parse_configuration(app):
    with open("configuration.json", encoding="utf-8") as f:
        configuration = json.load(f)

        app.config["SQLALCHEMY_DATABASE_URI"] = \
            configuration["database_url"]

        app.config["ALLOWED_EXTENSIONS"] = \
            configuration.get(
                "allowed_extensions",
                ["jpg", "png", "mov", "mp4", "mpg"]
            )
        
        app.config["MAX_CONTENT_LENGTH"] = \
            configuration.get(
                "maximum_content_length",
                1048576000 # 1000mb
            )
        
        app.config["UPLOAD_DURATIONS"] = \
            configuration["upload_durations"]
        
        app.config["PASSWORDS"] = configuration["passwords"]
