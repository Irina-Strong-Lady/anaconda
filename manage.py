import os
from app import create_app, db
from app.models import User, Role, Post, Follow, Permission, Comment
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand
from dotenv import load_dotenv


COV = None
if os.environ.get('ANACONDA_COVERAGE'):
    import coverage
    COV = coverage.coverage(branch=True, include='app/*')
    COV.start()

app = create_app(os.getenv('ANACONDA_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)


@app.shell_context_processor
def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role,
                Post=Post, Follow=Follow, Permission=Permission, Comment=Comment)


manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


@manager.command
def test(coverage=False):
    """Выполняет модульное тестирование."""
    if coverage and not os.environ.get('ANACONDA_COVERAGE'):
        import sys
        os.environ['ANACONDA_COVERAGE'] = '1'
        os.execvp(sys.executable, [sys.executable] + sys.argv)
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)
    if COV:
        COV.stop()
        COV.save()
        print('Coverage Summary:')
        COV.report()
        basedir = os.path.abspath(os.path.dirname(__file__))
        covdir = os.path.join(basedir, 'tmp/coverage')
        COV.html_report(directory=covdir)
        print('HTML version: file://%s/index.html' % covdir)
        COV.erase()


@manager.command
def profile(length=25, profile_dir=None):
    '''Запускает приложение в режиме профилирования кода'''
    from werkzeug.middleware.profiler import ProfilerMiddleware
    app.wsgi_app = ProfilerMiddleware(app.wsgi_app, restrictions=[length],
                                      profile_dir=profile_dir)
    app.run()


@manager.command
def deploy():
    '''Выполняет операции, связанные с развертыванием'''
    from flask_migrate import upgrade
    from app.models import Role, User

    # обновить базу данных до последней версии
    upgrade()

    # Создать роли для пользователей
    Role.insert_roles()

    # Объявить всех пользователей как читающих самих себя
    User.add_self_follows()


if __name__ == '__main__':
    manager.run()
