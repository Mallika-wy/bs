import time

import DrissionPage.errors
from DrissionPage import ChromiumPage
import re
import json

from ..plugin import message_queue


def get_tb_cookies(name, password):

    cp = ChromiumPage()
    cp.get("https://login.taobao.com/member/login.jhtml")
    time.sleep(1)
    cp.ele('css:#fm-login-id').clear()
    cp.ele('css:#fm-login-id').input(name)
    cp.ele('css:#fm-login-password').clear()
    cp.ele('css:#fm-login-password').input(password)
    cp.ele('css:.fm-button.fm-submit.password-login').click()

    return_data = {}
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
            'id': item['item_id'],
            'title': item['title'],
            'item_url': item['auctionURL'],
            'img_url': item['pic_path'],
            'price': item['price'],
            'nick': item['nick'],
            'procity': item.get('procity', ''),
            'type': 1
            # 'structuredUSPInfo': item.get('structuredUSPInfo', '')
        }
        if 'structuredUSPInfo' in item:
            specification = ""
            for item_info in item['structuredUSPInfo']:
                specification += item_info['propertyName'] + ':' + item_info['propertyValueName'] + '\n'
        else:
            specification = ""
        item_data['specification'] = specification
        return_data.append(item_data)
    return return_data


def get_jd_qrcode_and_cookie():
    cp = ChromiumPage()
    cp.set.window.max()
    cp.get("https://passport.jd.com/new/login.aspx")

    qrcode_base64 = cp.get_screenshot(as_base64=True, left_top=(800, 300), right_bottom=(1300, 700))

    message_queue.put(qrcode_base64)

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


def spider_jd(arg):
    cp = ChromiumPage()
    cookies = arg['cookies']
    cp.set.cookies(cookies)

    cp.get('https://www.jd.com/')
    cp.ele('xpath://*[@id="key"]').input(arg['searchText'])
    cp.ele('xpath://*[@id="search"]/div/div[2]/button').click()
    cp.wait.load_start(timeout=5)
    cp.scroll.to_bottom()
    items = cp.eles('xpath://li[@class="gl-item"]')
    return_data = []
    for item in items:
        id = item.attrs['data-sku']
        title = item('xpath://div[contains(@class,"p-name")]/a').text
        nick = item('xpath://a[@class="curr-shop hd-shopname"]').text
        item_url = item('xpath://div[contains(@class,"p-name")]/a').link
        img_url = item('xpath://div[contains(@class,"p-img")]/a/img').attrs['data-lazy-img']
        price = item('xpath://div[contains(@class,"p-price")]/strong/i').text
        item_data = {
            'id': id,
            'title': title,
            'item_url': item_url,
            'pic_url': img_url,
            'price': price,
            'nick': nick,
            'procity': '',
            'structuredUSPInfo': '',
            'type': 2
        }
        return_data.append(item_data)
    return return_data


def price_history(domain, item_id):
    cp = ChromiumPage()
    if domain == 'tmall':
        url = f'http://detail.tmallvvv.com/item.htm?id={item_id}'
    elif domain == 'jd':
        url = f'http://item.jdvvv.com/{item_id}.html'
    else:
        url = f'http://item.taobao.com/item.htm?id={item_id}'
    cp.get(url)
    time.sleep(2)
    canvas_element = cp.ele('@id=container')
    price_image = canvas_element.get_screenshot(as_base64=True)
    return price_image


def get_tb_price(url, cookie):
    cp = ChromiumPage()
    cp.set.cookies(cookie)
    cp.get(url)
    time.sleep(2)
    price_ele = cp.ele('.^priceWrap')
    price_text = price_ele.text
    match = re.search(r'[-+]?\d*\.?\d+', price_text)
    price_str = match.group(0)
    price = float(price_str)

    return price


def get_jd_price(url, cookie):
    cp = ChromiumPage()
    cp.set.cookies(cookie)
    cp.get(url)
    time.sleep(2)

    match = re.search(r'\d+', url)
    item_id = match.group(0)
    css_str = ".price.J-p-" + item_id
    price_ele = cp.ele(css_str)
    price_text = price_ele.text
    match = re.search(r'[-+]?\d*\.?\d+', price_text)
    price_str = match.group(0)
    price = float(price_str)

    return price


if __name__ == '__main__':
    cookies_string = get_tb_cookies('Mallika_wy', '2004wangyang')['cookies_string']
    spider_taobao(cookies_string)
