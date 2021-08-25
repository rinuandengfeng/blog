from flask import Flask
from flask_login import LoginManager

import settings

from exts import db, bootstrap, cache

app = Flask(__name__, template_folder='../templates', static_folder='../static')
config = {
    'CACHE_TYPE': 'redis',
    'CACHE_REDIS_HOST': '127.0.0.1',
    'CACHE_REDIS_PORT': 6379
}


def create_app():
    # 导入配置文件
    app.config.from_object(settings.ProductionConfig)
    # 初始化配置db
    db.init_app(app=app)
    # 初始化bootstarp
    bootstrap.init_app(app=app)
    # 导入蓝图
    from apps.article.views import article_bp1
    from apps.user.views import user_bp1
    # 初始化缓存文件
    cache.init_app(app=app, config=config)
    # 注册蓝图
    app.register_blueprint(user_bp1, url_prefix='/user')
    app.register_blueprint(article_bp1)
    return app
