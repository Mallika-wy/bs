from flask import Blueprint, request
import bcrypt
import time

from ..plugin import db, message_queue
from ..models import User, Account, Cookie
from ..utils.ApiResult import ApiResult
from ..utils.drission import get_tb_cookies, spider_taobao, get_jd_qrcode_and_cookie


bp = Blueprint('main', __name__)


@bp.route('/login', methods=['POST'])
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


@bp.route('/register', methods=['POST'])
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


@bp.route('/modifyUser', methods=['POST'])
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


@bp.route('/addTb', methods=['POST'])
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


@bp.route('/addJd', methods=['POST'])
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


@bp.route('/getQrcode', methods=['GET'])
def get_qrcode():
    timeout = 20
    end_time = time.time() + timeout
    qrcode_url = ''
    while time.time() < end_time:
        qrcode_url = message_queue.get(block=False)
        if qrcode_url:
            break
        time.sleep(1)  # 每隔1秒检查一次
    if not qrcode_url:
        result = ApiResult(code=401, message="没有获得到二维码")
        return result.make_response()

    result = ApiResult(code=200, message='成功得到二维码', data=qrcode_url)
    return result.make_response()


@bp.route('/search', methods=['GET'])
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
        # 'interval': my_config['interval'],
        # 'pages': my_config['pages'],
        'searchText': search_text
    }

    spider_taobao(arg)
    result = ApiResult(code=200, message='搜索成功')
    return result.make_response()
