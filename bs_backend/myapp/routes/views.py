from flask import Blueprint, request, current_app
import os
from fuzzywuzzy import fuzz
from queue import Empty

from ..plugin import db, message_queue, siwa, logger
from ..models import User, Account, Cookie, Item, Item_search, Search, Subscribe
from ..utils.ApiResult import ApiResult
from ..utils.email import send_email
from ..utils.drission import get_tb_cookies, get_tb_qrcode_and_cookie, spider_taobao, get_jd_qrcode_and_cookie, \
    spider_jd, get_tb_price, get_jd_price, price_history


bp = Blueprint('main', __name__)


@bp.route('/login', methods=['POST'])
@siwa.doc()
def login():
    data = request.get_json()
    print(data)
    name = data.get('name')
    password = data.get('password')

    user = User.query.filter_by(name=name).first()
    if user and user.password == password:
        cookie = "%d|%s|%s" % (user.id, user.name, user.password)
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


@bp.route('/getUserFromToken', methods=['GET'])
@siwa.doc()
def getUserFromToken():
    token = request.args.get('token')
    parts = token.split('|')
    user_id = int(parts[0])
    user = User.query.filter_by(id=user_id).first()
    if user:
        cookie = "%d|%s|%s" % (user.id, user.name, user.password)
        data = {
            'id': user.id,
            'name': user.name,
            'email': user.email,
            'phone': user.phone,
            'address': user.address,
            'sex': user.sex,
            'cookie': cookie
        }
        result = ApiResult(code=200, message='获取信息成功，自动登录', data=data)
        return result.make_response()
    else:
        result = ApiResult(code=401, message='获取失败')
        return result.make_response()


@bp.route('/register', methods=['POST'])
@siwa.doc()
def register():
    data = request.get_json()['user_info_dict']
    name = data['name']
    password = data['password']
    email = data['email']
    sex = data['sex']
    address = data['address']
    phone = data['phone']

    user = User.query.filter_by(name=name).first()
    if user:
        result = ApiResult(code=409, message='User name already exists')
        return result.make_response()

    user = User.query.filter_by(email=email).first()
    if user:
        result = ApiResult(code=409, message='Email already exists')
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
        result = ApiResult(code=201, message='User created successfully', data=data)
        return result.make_response()
    except Exception as e:
        db.session.rollback()


@bp.route('/modifyUser', methods=['POST'])
@siwa.doc()
def modify_user():
    data = request.get_json()
    user_id = data.get('id')
    modified_user = data.get('modifiedUser')
    user = User.query.filter_by(id=user_id).first()
    if user.name != modified_user['name']:
        count = User.query.filter_by(name=modified_user['name']).count()
        if count != 0:
            result = ApiResult(code=409, message='This name is already taken')
            return result.make_response()
    if user.email != modified_user['email']:
        count = User.query.filter_by(email=modified_user['email'])
        if count != 0:
            result = ApiResult(code=409, message='This email is already taken')
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
@siwa.doc()
def add_tb_account():
    # data = request.get_json()
    # user_id = data['user_id']
    # info_tb = data['info_tb']

    # data = get_tb_cookies(info_tb['t_name'], info_tb['t_password'])
    # if not data['OK']:
    #     result = ApiResult(code=401, message='淘宝账号添加失败，可能账号密码错误')
    #     return result.make_response()

    # cookies_to_delete = Cookie.query.filter_by(user_id=user_id, type=1).all()
    # for cookie in cookies_to_delete:
    #     db.session.delete(cookie)
    # db.session.commit()

    # cookies_string = data['cookies_string']
    # for cookie_string in cookies_string:
    #     new_cookie = Cookie(user_id=user_id, type=1, cookie=cookie_string)
    #     db.session.add(new_cookie)
    # db.session.commit()

    # old_account = Account.query.get(user_id)
    # if old_account:
    #     old_account.tb_name = info_tb['t_name']
    #     old_account.tb_password = info_tb['t_password']
    #     db.session.commit()
    # else:
    #     new_account = Account(
    #         user_id=user_id,
    #         tb_name=info_tb['t_name'],
    #         tb_password=info_tb['t_password']
    #     )
    #     db.session.add(new_account)
    #     db.session.commit()

    # result = ApiResult(code=200, message='添加淘宝账号成功')
    # return result.make_response()

    data = request.get_json()
    user_id = data['user_id']
    logger.info("get_tb_qrcode_and_cookie")
    data = get_tb_qrcode_and_cookie()
    if not data['OK']:
        result = ApiResult(code=401, message="超时，请重新尝试扫码登录")
        return result.make_response()

    cookies_to_delete = Cookie.query.filter_by(user_id=user_id, type=1).all()
    for cookie in cookies_to_delete:
        db.session.delete(cookie)
    db.session.commit()

    cookies_string = data['cookies_string']
    for cookie_string in cookies_string:
        new_cookie = Cookie(user_id=user_id, type=1, cookie=cookie_string)
        db.session.add(new_cookie)
    db.session.commit()

    old_account = Account.query.get(user_id)
    if old_account:
        old_account.tb_has_login = True
        db.session.commit()
    else:
        new_account = Account(
            user_id=user_id,
            tb_has_login=True
        )
        db.session.add(new_account)
        db.session.commit()

    result = ApiResult(code=200, message='添加淘宝账号成功')
    return result.make_response()



@bp.route('/addJd', methods=['POST'])
@siwa.doc()
def add_jd_account():
    data = request.get_json()
    user_id = data['user_id']

    data = get_jd_qrcode_and_cookie()
    if not data['OK']:
        result = ApiResult(code=401, message="超时，请重新尝试扫码登录")
        return result.make_response()

    cookies_to_delete = Cookie.query.filter_by(user_id=user_id, type=2).all()
    for cookie in cookies_to_delete:
        db.session.delete(cookie)
    db.session.commit()

    cookies_string = data['cookies_string']
    for cookie_string in cookies_string:
        new_cookie = Cookie(user_id=user_id, type=2, cookie=cookie_string)
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
@siwa.doc()
def get_qrcode():
    try:
        qrcode_base64 = message_queue.get(block=False)
        result = ApiResult(code=200, message='成功得到二维码', data=qrcode_base64)
    except Empty:
        result = ApiResult(code=401, message="二维码还没有爬取到，请等一会儿")
    return result.make_response()


@bp.route('/search', methods=['GET'])
@siwa.doc()
def search():
    user_id = request.args.get('id')
    search_text = request.args.get('searchText')
     
    searchs = Search.query.all()
    if searchs:
        search_id = -1
        max_similarity = -1
        for search in searchs:
            similarity = fuzz.ratio(search_text, search.search_text)
            if similarity > current_app.config['FUZZ_THRESHOLD']:
                if max_similarity < similarity:
                    max_similarity = similarity
                    search_id = search.search_id
        if search_id != -1:
            item_searchs = Item_search.query.filter_by(search_id=search_id).all()
            item_ids = [item_search.item_id for item_search in item_searchs]
            items = Item.query.filter(Item.item_id.in_(item_ids)).all()
            items_list = [
                {
                    'item_id': item.item_id,
                    'real_id': item.real_id,
                    'title': item.title,
                    'type': item.type,
                    'price': item.price,
                    'nick': item.nick,
                    'item_url': item.item_url,
                    'img_url': item.img_url,
                    'procity': item.procity
                }
                for item in items
            ]
            result = ApiResult(code=200, message='成功搜索到商品,从搜索库中查询', data=items_list)
            return result.make_response()

    cookies = Cookie.query.filter_by(user_id=user_id, type=1).all()
    if not cookies:
        result = ApiResult(code=401, message="您没有设置淘宝的账号，无法爬取淘宝商品数据")
        return result.make_response()
    cookies_list = [cookie.cookie for cookie in cookies]

    arg = {
        'cookies': cookies_list,
        # 'interval': my_config['interval'],
        # 'pages': my_config['pages'],
        'searchText': search_text
    }
    
    items_list = spider_taobao(arg)

    cookies = Cookie.query.filter_by(user_id=user_id, type=2).all()
    if not cookies:
        result = ApiResult(code=401, message="您没有设置京东的账号，无法爬取京东商品数据")
        return result.make_response()
    cookies_list = [cookie.cookie for cookie in cookies]
    arg['cookies'] = cookies_list
    items_list += spider_jd(arg)

    items = []
    for item_data in items_list:
        item = Item(
            real_id=item_data['real_id'],
            title=item_data['title'],
            item_url=item_data['item_url'],
            img_url=item_data['img_url'],
            price=item_data['price'],
            nick=item_data['nick'],
            procity=item_data['procity'],
            specification=item_data['specification'],
            type=item_data['type'],
        )
        print(item_data['item_url'])
        items.append(item)
    db.session.add_all(items)
    db.session.flush()

    search = Search(user_id=user_id, search_text=search_text)
    db.session.add(search)
    db.session.flush()

    for item in items:
        item_search = Item_search(item_id=item.item_id, search_id=search.search_id)
        db.session.add(item_search)

    db.session.commit()

    items_list = [
        {
            'item_id': item.item_id,
            'real_id': item.real_id,
            'title': item.title,
            'type': item.type,
            'price': item.price,
            'nick': item.nick,
            'item_url': item.item_url,
            'img_url': item.img_url,
            'procity': item.procity
        }
        for item in items
    ]
    result = ApiResult(code=200, message='搜索成功', data=items_list)
    return result.make_response()


@bp.route('/getDoc', methods=['GET'])
@siwa.doc()
def get_doc():
    # 获取当前文件的绝对路径
    current_file_path = os.path.abspath(__file__)

    # 获取当前文件所在的目录路径
    current_dir_path = os.path.dirname(current_file_path)

    # 构建 doc.md 的相对路径
    doc_md_path = os.path.join(current_dir_path, '..', 'doc.md')

    # 打开文件并读取内容
    with open(doc_md_path, 'r', encoding='utf-8') as file:
        markdown_content = file.read()

    print(markdown_content)
    result = ApiResult(code=200, message='获取数据成功', data=markdown_content)
    return result.make_response()


@bp.route('/history', methods=['GET'])
@siwa.doc()
def get_history():
    user_id = request.args.get('user_id')
    searchs = Search.query.filter_by(user_id=user_id).all()

    return_data = []
    for search in searchs:
        search_data = {'search_id': search.search_id, 'search_text': search.search_text}
        item_searchs = Item_search.query.filter_by(search_id=search.search_id).all()
        item_ids = [item_searchs.item_id for item_searchs in item_searchs]
        search_data['item_ids'] = item_ids
        search_data['num_items'] = len(item_ids)
        return_data.append(search_data)
    result = ApiResult(code=200, message='查找记录成功', data=return_data)
    return result.make_response()


@bp.route('/subscribe', methods=['POST'])
@siwa.doc()
def subscribe():
    data = request.get_json()
    user_id = data['user_id']
    item_id = data['item_id']

    user = User.query.filter_by(id=user_id).first()
    if not user:
        result = ApiResult(code=409, message='该用户不存在')
        return result.make_response()

    item = Item.query.filter_by(id=item_id).first()
    if not item:
        result = ApiResult(code=409, message='该商品不存在')
        return result.make_response()

    subscribe = Subscribe(user_id=user_id, item_id=item_id)
    db.session.add(subscribe)
    db.session.commit()

    result = ApiResult(code=200, message='订阅成功')
    return result.make_response()


@bp.route('/checkSubscribe', methods=['POST'])
@siwa.doc()
def check_subscribe():
    data = request.get_json()
    user_id = data['user_id']
    user = User.query.filter_by(id=user_id).first()

    cookies = Cookie.query.filter_by(user_id=user_id, type=1).all()
    if not cookies:
        result = ApiResult(code=401, message="您没有设置淘宝的账号，无法爬取淘宝商品数据")
        return result.make_response()
    cookies_tb_list = [cookie.cookie for cookie in cookies]

    cookies = Cookie.query.filter_by(user_id=user_id, type=2).all()
    if not cookies:
        result = ApiResult(code=401, message="您没有设置京东的账号，无法爬取京东商品数据")
        return result.make_response()
    cookies_jd_list = [cookie.cookie for cookie in cookies]

    subscribes = Subscribe.query.filter_by(user_id=user_id).all()
    item_ids = [subscribe.item_id for subscribe in subscribes]
    items = Item.query.filter(Item.item_id.in_(item_ids)).all()

    content = f'尊敬的用户{user.name}, 您关注的如下商品已经降价:' + os.linesep
    i = 0
    for item in items:
        if item.type == 1:
            new_price = get_tb_price(item.item_url, cookies_jd_list)
        else:
            new_price = get_jd_price(item.item_url, cookies_tb_list)

        if new_price < item.price:
            i = i + 1
            content += f'{i}: {item.title}价格已下降至{new_price}元，请及时购买' + os.linesep

    if i == 0:
        result = ApiResult(code=200, message='没有检测到商品降价')
        return result.make_response()
    else:
        send_email({'email': user.email, 'content': content})
        result = ApiResult(code=200, message='检测到商品降价, 具体信息已发送给您的邮箱')
        return result.make_response()


@bp.route('/searchItem', methods=['GET'])
@siwa.doc()
def search_item():
    user_id = request.args.get('user_id')
    item_id = request.args.get('item_id')
    #  根据id来查找item表中特定数据
    item = Item.query.filter_by(item_id=item_id).first()
    if item is None:
        result = ApiResult(code=401, message='没有找到该商品')
        return result.make_response()
    if item.price == -1:
        cookies = Cookie.query.filter_by(user_id=user_id, type=1).all()
        if not cookies:
            result = ApiResult(code=401, message="您没有设置淘宝的账号，无法爬取淘宝商品数据")
            return result.make_response()
        cookies_tb_list = [cookie.cookie for cookie in cookies]
        price = get_tb_price(item.item_url, cookies_tb_list)
        item.price = price
        db.session.add(item)
    data = {}
    if 'tmall' in item.item_url:
        data = price_history('tmall', item.real_id)
    elif 'taobao' in item.item_url:
        data = price_history('taobao', item.real_id)
    elif 'jd' in item.item_url:
        data = price_history('jd', item.real_id)
    return_data = {
        'id': item.item_id,
        'real_id': item.real_id,
        'title': item.title,
        'price': item.price,
        'nick': item.nick,
        'item_url': item.item_url,
        'img_url': item.img_url,
        'procity': item.procity,
        'specification': item.specification
    }
    if not data['OK']:
        return_data['history_image'] = ''
    else:
        return_data['history_image'] =data['price_image']
    result = ApiResult(code=200, message='详情获取成功', data=return_data)
    return result.make_response()


@bp.route('/getItemsFromSearchID', methods=['GET'])
@siwa.doc()
def get_items_from_search_id():
    user_id = request.args.get('user_id')
    search_id = request.args.get('search_id')

    item_searchs = Item_search.query.filter_by(search_id=search_id).all()
    item_ids = [item_searchs.item_id for item_searchs in item_searchs]
    items = Item.query.filter(Item.item_id.in_(item_ids)).all()
    items_list = [
        {
            'item_id': item.item_id,
            'real_id': item.real_id,
            'title': item.title,
            'type': item.type,
            'price': item.price,
            'nick': item.nick,
            'item_url': item.item_url,
            'img_url': item.img_url,
            'procity': item.procity
        }
        for item in items
    ]
    result = ApiResult(code=200, message='获取成功', data=items_list)
    return result.make_response()
