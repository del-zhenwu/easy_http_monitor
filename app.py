# -*- coding: utf-8 -*-
from flask import Flask
from flask_apscheduler import APScheduler
from flask_socketio import SocketIO
from config import load_config

socketio = SocketIO()


def create_app():
    app = Flask('easy_http')
    # configure app
    config = load_config()
    app.config.from_object(config)
    # configure hook
    configure_hook(app)
    # configure blueprints
    configure_blueprints(app)
    # configure extensions such as db engine
    # configure_db(app)
    configure_scheduler(app)
    # configure websocket
    # configure_websocket(app)
    socketio.init_app(app)

    return app


def configure_hook(app):

    @app.before_request
    def before_request():
        pass


def configure_blueprints(app):
    from config_api.views import mod as api_mod
    # from dash.views import mod as dash_mod
    app.register_blueprint(api_mod)
    # app.register_blueprint(dash_mod)


def configure_scheduler(app):
    scheduler = APScheduler()
    scheduler.init_app(app)
    scheduler.start()


# def configure_websocket(app):
#     from flask_socketio import SocketIO
#     socketio = SocketIO()
#     socketio.init_app(app)
