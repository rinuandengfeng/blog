from flask import url_for
from flask_login import LoginManager
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from werkzeug.utils import redirect

from apps.user.models import *
from apps.article.models import *

from apps import create_app
from exts import db

app = create_app()
manager = Manager(app=app)
# 命令工具
migrate = Migrate(app=app, db=db)
manager.add_command('db', MigrateCommand)

@app.route('/')
def index():
    return redirect(url_for('user.index'))

if __name__ == '__main__':
    manager.run()
