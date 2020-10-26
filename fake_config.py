import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'removed_for_github'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    VAPID_PUBLIC_KEY = "removed_for_github"
    VAPID_PRIVATE_KEY = "removed_for_github"
    VAPID_CLAIM_EMAIL = "removed_for_github"
