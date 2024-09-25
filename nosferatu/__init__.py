import os
from uuid import uuid4
from datetime import datetime, timedelta
from flask import Flask, render_template, request


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="dev",
        DATABASE=os.path.join(app.instance_path, "flaskr.sqlite"),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)

        # TODO: figure out config later
        app.config.from_object("nosferatu.temp_config")
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # init db
    from . import db

    db.init_app(app)

    # init auth
    from . import auth

    app.register_blueprint(auth.bp)

    # init scheduler
    from . import scheduler

    scheduler.init_app(app)

    # init wemos
    from . import wemos

    app.register_blueprint(wemos.bp)

    @app.route("/", methods=["GET"])
    def index() -> str:
        return render_template(
            "index.html",
        )

    @app.route("/privacy", methods=["GET"])
    def privacy() -> str:
        return render_template("privacy.html")

    @app.route("/toggle/<uuid:key>", methods=["GET"])
    def toggle(key: str):
        toggle_mode = request.args.get("mode", type=str)
        delay_seconds = request.args.get("delay", type=int)

        device = None
        for wemo in app.config["WEMOS"]:
            if wemo.key == key:
                device = wemo
                break

        if not device:
            return "device was not found", 404

        if delay_seconds:
            scheduler.scheduler.add_job(
                str(uuid4()),
                lambda: wemos.process_toggle(device, toggle_mode),
                trigger="date",
                run_date=datetime.now() + timedelta(seconds=delay_seconds),
            )
            return f"{device.name} was scheduled in {delay_seconds} seconds"
        else:
            return wemos.process_toggle(device, toggle_mode)

    return app
