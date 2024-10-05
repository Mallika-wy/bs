from extension import db


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(30), unique=True, nullable=False)
    sex = db.Column(db.Integer, nullable=False, default=1)  # 默认值为男性
    address = db.Column(db.String(50), nullable=True)
    phone = db.Column(db.String(20), nullable=True)

    def __repr__(self):
        return f'<User {self.name}>'
