from flask import Flask
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from apps.user.models import User
from apps.article.models import Article
from apps import create_app
from exts import db

app = create_app()
manager = Manager(app=app)

# 命令工具
migrate = Migrate(app=app, db=db)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
