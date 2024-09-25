from flask_apscheduler import APScheduler


scheduler = APScheduler()


def init_app(app):
    scheduler.init_app(app)
    scheduler.start()
