from datetime import datetime

from exts import db


class Article_type(db.Model):
    __tablename__ = 'article_type'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    type_name = db.Column(db.String(20), nullable=True)
    article = db.relationship('Article', backref='articletype')


class Article(db.Model):
    __tablename__ = 'article'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(50), nullable=False)  # 发表标题
    content = db.Column(db.BLOB, nullable=False)  # 发表内容
    padatetime = db.Column(db.DateTime, default=datetime.now)  # 发表时间
    click_num = db.Column(db.Integer, default=0)  # 阅读量
    save_num = db.Column(db.Integer, default=0)  # 收藏量
    love_num = db.Column(db.Integer, default=0)  # 点赞量
    # 外键  同步到数据库的外键关系
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    # 发表文章时必须选择是什么类
    type_id = db.Column(db.Integer, db.ForeignKey('article_type.id'), nullable=False)
    # 建立文章表与评论表的关系    文章的评论
    comments = db.relationship('Comment', backref='article')  # 文章的评论
    # 根据作者找文章 ，两个不能同时有
    # user = db.relationship('User', backref='articles')
    # 根据文章找作者
    # articles = db.relationship('Article',backref = 'user',)


class Comment(db.Model):
    # 生自定义表的名字
    __tablename__ = 'comment'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    comment = db.Column(db.String(255), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    article_id = db.Column(db.Integer, db.ForeignKey('article.id'))
    cdatetime = db.Column(db.DateTime, default=datetime.now())

    def __str__(self):
        return self.comment
