# -*- coding: utf-8 -*-
"""Application configuration."""
import os


class BaseConfig:
    """Base configuration."""
    DEBUG = True
    SECRET_KEY = 'hK85B88WNdO82xwDqk2h'
    ENV = 'base'
    APP_DIR = os.path.abspath(os.path.dirname(__file__))  # This directory
    UPLOAD_FOLDER = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'media')
    PROJECT_ROOT = os.path.abspath(os.path.join(APP_DIR, os.pardir))
    # this app is designed to run in isolated from outside env world
    CORS_ORIGIN_WHITELIST = [
        '*',
    ]


class ProdConfig(BaseConfig):
    ENV = 'prod'
    DEBUG = False


class DevConfig(BaseConfig):
    ENV = 'dev'
    DEBUG = True


class TestConfig(BaseConfig):
    ENV = 'test'
    TESTING = True
    DEBUG = True
