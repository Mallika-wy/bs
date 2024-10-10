import DrissionPage.errors
from DrissionPage import ChromiumPage
import re
import json

from ..plugin import message_queue


def get_tb_cookies(name, password):
    cp = ChromiumPage()
    cp.get("https://login.taobao.com/member/login.jhtml")
    cp.ele('css:#fm-login-id').clear()
    cp.ele('css:#fm-login-id').input(name)
    cp.ele('css:#fm-login-password').clear()
    cp.ele('css:#fm-login-password').input(password)
    cp.ele('css:.fm-button.fm-submit.password-login').click()

    is_timeout = False
    return_data = {}
    try:
        cp.wait.load_start(timeout=20, raise_err=True)
    except DrissionPage.errors.WaitTimeoutError:
        is_timeout = True
        return_data['OK'] = False

    if not is_timeout:
        cookies_string = []
        cookies = cp.cookies()
        for cookie in cookies:
            cookie_string = ''
            for key, value in cookie.items():
                sub_str = "%s=%s; " % (key, value)
                cookie_string = cookie_string + sub_str
            cookie_string = cookie_string.rstrip()
            cookies_string.append(cookie_string)
        return_data['cookies_string'] = cookies_string
        return_data['OK'] = True

    cp.close()
    return return_data


def spider_taobao(arg):
    cp = ChromiumPage()
    cookies = arg['cookies']
    cp.set.cookies(cookies)

    cp.get('https://www.taobao.com/')
    cp.ele('css:#q').input(arg['searchText'])
    cp.ele('css:.btn-search.tb-bg').click()
    cp.listen.start('h5/mtop.relationrecommend.wirelessrecommend.recommend/2.0')
    cp.refresh()
    list_data_packet = cp.listen.wait(count=2)

    data_packet = list_data_packet[1]
    response = data_packet.response
    mtopjsonp = response.body
    mtopjson = re.findall('mtopjsonp\d+\((.*)\)', mtopjsonp)[0]
    mtop_data = json.loads(mtopjson)
    itemsArray = mtop_data['data']['itemsArray']

    return_data = []
    for item in itemsArray:
        item_data = {
            'auctionURL': item['auctionURL'],
            'pic_url': item['pic_url'],
            'price': item['priceWap'],
            'nick': item['nick']
        }
        return_data.append(item_data)
    return return_data


def get_jd_qrcode_and_cookie():
    cp = ChromiumPage()
    cp.get("https://passport.jd.com/new/login.aspx")
    qrcode_ele = cp.ele('@id=passport-main-qrcode-img')
    qrcode_url = qrcode_ele.attr('src')
    message_queue.put(qrcode_url)

    is_timeout = False
    return_data = {}
    try:
        cp.wait.load_start(timeout=60, raise_err=True)
    except DrissionPage.errors.WaitTimeoutError:
        is_timeout = True
        return_data['OK'] = False

    if not is_timeout:
        cookies_string = []
        cookies = cp.cookies()
        for cookie in cookies:
            cookie_string = ''
            for key, value in cookie.items():
                sub_str = "%s=%s; " % (key, value)
                cookie_string = cookie_string + sub_str
            cookie_string = cookie_string.rstrip()
            cookies_string.append(cookie_string)
        return_data['cookies_string'] = cookies_string
        return_data['OK'] = True

    cp.close()
    return return_data
