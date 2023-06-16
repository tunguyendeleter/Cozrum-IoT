from flask import Flask,request,Blueprint

from library.BOOK.controller import books


def create_app(config_file="config.py"):
    app=Flask(__name__)
    app.config.from_pyfile(config_file)
    app.register_blueprint(books)
    print(app.config["SECRET_KEY"])
    return app




