from flask import Flask
from flask_login import LoginManager

import settings


from exts import db, bootstrap

app = Flask(__name__, template_folder='../templates', static_folder='../static')


def create_app():
    # 导入配置文件
    app.config.from_object(settings.DevelopmentConfig)
    # 初始化配置db
    db.init_app(app=app)
    # 初始化bootstarp
    bootstrap.init_app(app=app)
    # 导入蓝图
    from apps.article.views import article_bp1
    from apps.user.views import user_bp1
    # 注册蓝图
    app.register_blueprint(user_bp1, url_prefix='/user')
    app.register_blueprint(article_bp1)
    return app
