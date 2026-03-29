from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from flask import Flask, jsonify
from .exceptions import ValidationError
from ..views import api_blueprint, api_doc


def planogram_errorhandler(error):
    return jsonify({"message": error.message}), 400


def handle_error(err):
    headers = err.data.get("headers", None)
    messages = err.data.get("messages", ["Invalid request."])
    if headers:
        return jsonify(messages), 400
    else:
        return jsonify(messages), 400


def create_app(config='ai_service.api.settings.BaseConfig'):
    app = Flask(__name__)
    app.config.from_object(config)
    app.config.from_envvar('PLANOGRAM_SETTINGS', silent=True)
    app.errorhandler(422)(handle_error)
    app.errorhandler(400)(handle_error)
    app.errorhandler(ValidationError)(planogram_errorhandler)
    app.register_blueprint(api_blueprint)

    app.config.update({
        'APISPEC_SPEC': APISpec(
            title='Planogram Ai Service',
            version='v1',
            plugins=[MarshmallowPlugin()],
            openapi_version='3.0.2',
        ),
        'APISPEC_SWAGGER_URL': '/swagger/',
    })
    api_doc.init_app(app)
    api_doc.register_existing_resources()

    return app
