import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    TEMPLATES_AUTO_RELOAD = True
    SECRET_KEY = "TESTC?(JgtSEC?KEY"

    # use ./app.db or DATABASE_URL
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Pagination var
    POSTS_PER_PAGE = 2
