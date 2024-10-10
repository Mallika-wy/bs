from .plugin import db


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(30), unique=True, nullable=False)
    sex = db.Column(db.Integer, nullable=False, default=1)  # 默认值为男性
    address = db.Column(db.String(50), nullable=True)
    phone = db.Column(db.String(20), nullable=True)

    def __repr__(self):
        return f'<User {self.name}>'


class Account(db.Model):
    __tablename__ = 'account'

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    tb_name = db.Column(db.String(30), nullable=True)
    tb_password = db.Column(db.String(30), nullable=True)
    jd_has_login = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<TBJD {self.user_id}>'


class Cookie(db.Model):
    __tablename__ = 'cookie'

    cookie_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    type = db.Column(db.Integer, nullable=False)
    cookie = db.Column(db.String(1000), nullable=False)
