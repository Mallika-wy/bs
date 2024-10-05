from flask import Flask
from flask_migrate import Migrate
import click
from flask import request
import bcrypt

from extension import db, cors
from models import User
from utils import ApiResult


app = Flask(__name__)

# 配置数据库连接信息
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:2004wangyang@localhost/bs'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
cors.init_app(app)
migrate = Migrate(app, db)


@app.cli.command()  # 注册为命令，可以传入 name 参数来自定义命令
@click.option('--drop', is_flag=True, help='Create after drop.')  # 设置选项
def initdb(drop):
    """Initialize the database."""
    if drop:
        db.drop_all()
        click.echo('Drop tables.')
    else:
        db.create_all()
        click.echo('Initialized database.')

        # 在 users 表中添加一条数据
        user = User(
            name='test01',
            password='test0101_',
            email='test01@gmail.com',
            sex=1,
            address='zhejiang hangzhou',
            phone='12345678911'
        )
        db.session.add(user)
        try:
            db.session.commit()
            click.echo('Added default user.')
        except Exception as e:
            db.session.rollback()
            click.echo('Error adding default user: ' + str(e))


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(name=username).first()
    if user and user.password == password:
        password_bytes = password.encode('utf-8')
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password_bytes, salt)
        cookie = "%d|%s|%s" % (user.id, user.name, hashed_password)
        data = {
            'id': user.id,
            'cookie': cookie
        }
        result = ApiResult(code=200, message='Login successful', data=data)
        return result.make_response()
    elif user:
        result = ApiResult(code=401, message='password error')
        return result.make_response()
    else:
        result = ApiResult(code=401, message='Invalid credentials')
        return result.make_response()
