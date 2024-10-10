from flask import Flask
from flask_migrate import Migrate
import click
from flask import request
import bcrypt
import redis

from extension import db, cors
from models import User, Account, Cookie
from utils import ApiResult, my_config
from drission import spider_taobao, get_tb_cookies, get_jd_qrcode_and_cookie


app = Flask(__name__)

# 配置数据库连接信息
app.config['SQLALCHEMY_DATABASE_URI'] = my_config['SQLALCHEMY_DATABASE_URI']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = my_config['SQLALCHEMY_TRACK_MODIFICATIONS']
db.init_app(app)
cors.init_app(app)
migrate = Migrate(app, db)
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)


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
    print(data)
    name = data.get('name')
    password = data.get('password')

    user = User.query.filter_by(name=name).first()
    if user and user.password == password:
        password_bytes = password.encode('utf-8')
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password_bytes, salt)
        cookie = "%d|%s|%s" % (user.id, user.name, hashed_password)
        data = {
            'id': user.id,
            'name': user.name,
            'email': user.email,
            'phone': user.phone,
            'address': user.address,
            'sex': user.sex,
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


@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    name = data.get('name')
    password = data.get('password')
    email = data.get('email')
    sex = data.get('sex')
    address = data.get('address')
    phone = data.get('phone')

    user = User.query.filter_by(name=name).first()
    if user:
        result = ApiResult(code=401, message='User name already exists')
        return result.make_response()

    user = User.query.filter_by(email=email).first()
    if user:
        result = ApiResult(code=401, message='Email already exists')
        return result.make_response()

    new_user = User(name=name, password=password, email=email, sex=sex, address=address, phone=phone)
    db.session.add(new_user)
    try:
        db.session.commit()
        data = {
            'id': new_user.id,
            'name': new_user.name,
            'email': new_user.email,
            'phone': new_user.phone,
            'address': new_user.address
        }
        result = ApiResult(code=200, message='User created successfully', data=data)
        return result.make_response()
    except Exception as e:
        db.session.rollback()
        click.echo('Error adding user: ' + str(e))


@app.route('/modifyUser', methods=['POST'])
def modify_user():
    data = request.get_json()
    user_id = data.get('id')
    modified_user = data.get('modifiedUser')
    user = User.query.filter_by(id=user_id).first()
    if user.name != modified_user['name']:
        count = User.query.filter_by(name=modified_user['name']).count()
        if count != 0:
            result = ApiResult(code=401, message='This name is already taken')
            return result.make_response()
    if user.email != modified_user['email']:
        count = User.query.filter_by(email=modified_user['email'])
        if count != 0:
            result = ApiResult(code=401, message='This email is already taken')
            return result.make_response()

    user.name = modified_user['name']
    user.email = modified_user['email']
    user.phone = modified_user['phone']
    user.address = modified_user['address']
    user.sex = modified_user['sex']
    db.session.commit()
    data = {
        'id': user.id,
        'name': user.name,
        'email': user.email,
        'phone': user.phone,
        'address': user.address,
        'sex': user.sex
    }
    result = ApiResult(code=200, message='User created successfully', data=data)
    return result.make_response()


@app.route('/addTb', methods=['POST'])
def add_tb_account():
    data = request.get_json()
    user_id = data['user_id']
    info_tb = data['info_tb']

    data = get_tb_cookies(info_tb['t_name'], info_tb['t_password'])
    if not data['OK']:
        result = ApiResult(code=401, message='淘宝账号添加失败，可能账号密码错误')
        return result.make_response()

    cookies_string = data['cookies_string']
    for cookie_string in cookies_string:
        new_cookie = Cookie(user_id=data['id'], type=1, cookie=cookie_string)
        db.session.add(new_cookie)
    db.session.commit()

    old_account = Account.query.get(user_id)
    if old_account:
        old_account.tb_name = info_tb['tb_name']
        old_account.tb_password = info_tb['tb_password']
        db.session.commit()
    else:
        new_account = Account(
            user_id=user_id,
            tb_name=info_tb['tb_name'],
            tb_password=info_tb['tb_password']
        )
        db.session.add(new_account)
        db.session.commit()

    result = ApiResult(code=200, message='添加淘宝账号成功')
    return result.make_response()


@app.route('/addJd', methods=['POST'])
def add_jd_account():
    data = request.get_json()
    user_id = data['user_id']

    data = get_jd_qrcode_and_cookie()
    if not data['OK']:
        result = ApiResult(code=401, message="超时，请重新尝试扫码登录")
        return result.make_response()

    cookies_string = data['cookies_string']
    for cookie_string in cookies_string:
        new_cookie = Cookie(user_id=data['id'], type=2, cookie=cookie_string)
        db.session.add(new_cookie)
    db.session.commit()

    old_account = Account.query.get(user_id)
    if old_account:
        old_account.jd_has_login = True
        db.session.commit()
    else:
        new_account = Account(
            user_id=user_id,
            jd_has_login=True
        )
        db.session.add(new_account)
        db.session.commit()

    result = ApiResult(code=200, message='添加京东账号成功')
    return result.make_response()



@app.route('/getQrcode', methods=['GET'])
def get_qrcode():
    while True:
        qrcode_url = redis_client.get('qrcode_url')
        if qrcode_url:
            redis_client.delete('qrcode_url')
            break
    data = {
        'qrcode_url': qrcode_url
    }
    result = ApiResult(code=200, message='成功得到二维码', data=data)
    return result.make_response()


@app.route('/search', methods=['GET'])
def search():
    user_id = request.args.get('id')
    search_text = request.args.get('searchText')

    cookies = Cookie.query.filter_by(user_id=user_id, type=1).all()
    if not cookies:
        result = ApiResult(code=401, message="您没有设置淘宝和京东的账号，无法爬取数据")
        return result.make_response()

    cookies_list = [cookie.cookie for cookie in cookies]

    arg = {
        'cookies': cookies_list,
        'interval': my_config['interval'],
        'pages': my_config['pages'],
        'searchText': search_text
    }

    spider_taobao(arg)
    result = ApiResult(code=200, message='搜索成功')
    return result.make_response()

