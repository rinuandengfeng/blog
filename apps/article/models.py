from datetime import datetime

from exts import db


class Article(db.Model):
    __tablename__ = 'article'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(50), nullable=False)  # 发表标题
    content = db.Column(db.Text, nullable=False)  # 发表内容
    padatetime = db.Column(db.DateTime, default=datetime.now)  # 发表时间
    click_num = db.Column(db.Integer, default=0)  # 阅读量
    save_num = db.Column(db.Integer, default=0)  # 收藏量
    love_num = db.Column(db.Integer, default=0)  # 点赞量
    # 外键  同步到数据库的外键关系
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

