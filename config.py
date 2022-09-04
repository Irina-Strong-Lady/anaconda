import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'e953491d3845fa0167c0b5d6b8b970a1b0ae32b7'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    ANACONDA_MAIL_SUBJECT_PREFIX = '[Anaconda]'
    ANACONDA_MAIL_SENDER = os.environ.get('MAIL_USERNAME')
    ANACONDA_ADMIN = os.environ.get('ANACONDA_ADMIN')
    BOOTSTRAP_SERVE_LOCAL = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ANACONDA_POSTS_PER_PAGE = 20
    ANACONDA_FOLLOWERS_PER_PAGE = 50
    ANACONDA_COMMENTS_PER_PAGE = 30
    MOMENT_DEFAULT_FORMAT = 'DD.MM.YYYY'
    SQLALCHEMY_RECORD_QUERIES = True
    ANACONDA_SLOW_DB_QUERY_TIME = 0.5
    SSL_REDIRECT = False
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = os.environ.get('MAIL_PORT')
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')

    @staticmethod
    def init_app(app):
        pass

    @staticmethod
    def create_db():
        from sqlalchemy import create_engine
        from sqlalchemy_utils import database_exists, create_database
    
        if os.environ.get('DATABASE_URL') != None:
            engine = create_engine(os.environ.get('DATABASE_URL'))
            if not database_exists(engine.url):
                create_database(engine.url)
            print(database_exists(engine.url))
            return create_database



class DevelopmentConfig(Config):
    DEBUG = True    
    MAIL_USE_TLS = True
    
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')

    Config.create_db()


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')
    WTF_CSRF_ENABLED = False

    Config.create_db()


class ProductionConfig(Config):
    
    DEBUG = False
    MAIL_USE_TLS = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data.sqlite')

    Config.create_db()


    @classmethod
    def init_app(cls, app):
        Config.init_app(app)

        # уведомление администратора об ошибках по email
        import logging
        from logging.handlers import SMTPHandler
        credentials = None
        secure = None
        if getattr(cls, 'MAIL_USERNAME', None) is not None:
            credentials = (cls.MAIL_USERNAME, cls.MAIL_PASSWORD)
            if getattr(cls, 'MAIL_USE_TLS', None):
                secure = ()
        mail_handler = SMTPHandler(
            mailhost=(cls.MAIL_SERVER, cls.MAIL_PORT),
            fromaddr=cls.ANACONDA_MAIL_SENDER,
            toaddrs=[cls.ANACONDA_ADMIN],
            subject=cls.ANACONDA_MAIL_SUBJECT_PREFIX + ' Application Error',
            credentials=credentials,
            secure=secure)
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)

        # Перехват заголовков прокси-сервера
        try:
            from werkzeug.middleware.proxy_fix import ProxyFix
        except ImportError:
            from werkzeug.contrib.fixers import ProxyFix
        app.wsgi_app = ProxyFix(app.wsgi_app)

        # Журналирование в потоке stderr
        import logging
        from logging import StreamHandler
        file_handler = StreamHandler()
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)


class HerokuConfig(ProductionConfig):
    SSL_REDIRECT = True if os.environ.get('DYNO') else False
    @classmethod
    def init_app(cls, app):
        ProductionConfig.init_app(app)

        # Перехват заголовков прокси-сервера
        try:
            from werkzeug.middleware.proxy_fix import ProxyFix
        except ImportError:
            from werkzeug.contrib.fixers import ProxyFix
        app.wsgi_app = ProxyFix(app.wsgi_app)

        # Журналирование в потоке stderr
        import logging
        from logging import StreamHandler
        file_handler = StreamHandler()
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)


class DockerConfig(ProductionConfig):

    @classmethod
    def init_app(cls, app):
        ProductionConfig.init_app(app)

        # Журналирование в потоке stderr
        import logging
        from logging import StreamHandler
        file_handler = StreamHandler()
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler) 


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'heroku' : HerokuConfig,
    'docker' : DockerConfig,

    'default': DevelopmentConfig
}
