import time

import DrissionPage.errors
from DrissionPage import ChromiumPage, ChromiumOptions
import re
import json
from bs4 import BeautifulSoup

from ..plugin import message_queue, logger


browser_instance = None

def get_browser():
    global browser_instance
    if browser_instance is None:
        co = ChromiumOptions()
        co = co.set_argument('--no-sandbox')  # 关闭沙箱模式, 解决`$DISPLAY`报错
        co = co.headless(True)
        browser_instance = ChromiumPage(co)
    return browser_instance

def get_tb_cookies(name, password):
    cp = get_browser()
    cp.get("https://login.taobao.com/member/login.jhtml")
    time.sleep(1)
    cp.ele('css:#fm-login-id').clear()
    cp.ele('css:#fm-login-id').input(name)
    cp.ele('css:#fm-login-password').clear()
    cp.ele('css:#fm-login-password').input(password)
    cp.ele('css:.fm-button.fm-submit.password-login').click()
    logger.info("点击行为完成")

    time.sleep(2)

    return_data = {}
    error_element = cp.ele('css:.login-error-msg', timeout=1)

    if error_element and error_element.text == '账密错误':
        return_data['OK'] = False
        return return_data

    cookies_string = []
    cookies = cp.cookies()
    logger.info(cookies)
    for cookie in cookies:
        cookie_string = ''
        for key, value in cookie.items():
            sub_str = "%s=%s; " % (key, value)
            cookie_string = cookie_string + sub_str
        cookie_string = cookie_string.rstrip()
        cookies_string.append(cookie_string)
    return_data['cookies_string'] = cookies_string
    return_data['OK'] = True

    return return_data


def get_tb_qrcode_and_cookie():
    cp = get_browser()
    cp.set.window.max()
    cp.get("https://login.taobao.com/member/login.jhtml")

    qrcode_ele = cp.ele('css:.qrcode-login')
    logger.info(qrcode_ele)
    qrcode_base64 = qrcode_ele.get_screenshot(as_base64=True)

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
        
    return return_data


def spider_taobao(arg):
    cp = get_browser()

    cookies = arg['cookies']
    cp.set.cookies(cookies)

    cp.get('https://www.taobao.com/')
    cp.ele('css:#q').input(arg['searchText'])
    cp.ele('css:.btn-search.tb-bg').click()

    tab = cp.get_tab()
    tab.set.scroll.smooth(on_off=True)
    tab.scroll.to_half()
    cp.wait(1)
    tab.scroll.to_bottom()
    cp.wait(1)
    tab.scroll.to_half()
    time.sleep(1)

    content_items_wrapper = cp.ele('xpath://*[@id="content_items_wrapper"]')
    items = content_items_wrapper.children()
    i = 0
    return_data = []
    for item in items:
        if i == 0:
            i = i+1
            continue
        item = item.child()
        id_str = item.attrs['id'].split('_')[-1]
        id = int(id_str)
        item_url = item.attrs['href']
        if 'taobao' in item_url:
            item_url = f'//item.taobao.com/item.htm?id={id}'
        else:
            item_url = f'//detail.tmall.com/item.htm?id={id}'
        item = item.child()
        img_ele_parent = item.child().child()
        sbsbsbs = img_ele_parent.children()
        print(len(sbsbsbs))
        if len(sbsbsbs) == 3:
            continue
        img_ele = item.child().child().child()
        img_url = img_ele.attrs['src']
        if len(img_url) > 200:
            continue
        title = item.ele('xpath://div[1]/div[2]/div/span').text
        price = item.ele('xpath://div[1]/div[4]/div[1]').text
        price = float(price)

        has_priocity2 = len(item.ele('xpath://div[1]/div[4]').children()) == 3
        priocity = item.ele('xpath://div[1]/div[4]/div[2]').text
        if has_priocity2:
            priocity = priocity+item.ele('xpath://div[1]/div[4]/div[3]').text
        nick_parent = item.ele('xpath://div[3]/div[1]/a/div')
        has_nick2 = len(nick_parent.children()) == 2
        if has_nick2:
            nick = item.ele('xpath://div[3]/div[1]/a/div/span[2]').text
        else:
            nick = item.ele('xpath://div[3]/div[1]/a/div/span').text
        item_data = {
            'real_id': id,
            'title': title,
            'item_url': item_url,
            'img_url': img_url,
            'price': price,
            'nick': nick,
            'procity': priocity,
            'specification': '',
            'type': 1
        }
        return_data.append(item_data)
        print(id)
        print(nick)
    return return_data
    # cp.listen.start('h5/mtop.relationrecommend.wirelessrecommend.recommend/2.0')
    # response_list = cp.listen.wait(count=2)
    # mtopjsonp = response_list[1].response.body
    # mtopjson = re.findall('mtopjsonp\d+\((.*)\)', mtopjsonp)[0]
    # mtop_data = json.loads(mtopjson)
    # itemsArray = mtop_data['data']['itemsArray']
    # for item in itemsArray:
    #     soup = BeautifulSoup(item['title'], 'lxml')
    #     item['title'] = soup.get_text()
    #     item_data = {
    #         'real_id': item['item_id'],
    #         'title': item['title'],
    #         'item_url': item['auctionURL'],
    #         'img_url': item['pic_path'],
    #         'price': item['price'],
    #         'nick': item['nick'],
    #         'procity': item.get('procity', ''),
    #         'type': 1
    #         # 'structuredUSPInfo': item.get('structuredUSPInfo', '')
    #     }
    #     if 'structuredUSPInfo' in item:
    #         specification = ""
    #         for item_info in item['structuredUSPInfo']:
    #             specification += item_info['propertyName'] + ':' + item_info['propertyValueName'] + '\n'
    #     else:
    #         specification = ""
    #     item_data['specification'] = specification
    #     return_data.append(item_data)



def get_jd_qrcode_and_cookie():
    cp = get_browser()
    cp.set.window.max()
    cp.get("https://passport.jd.com/new/login.aspx")

    qrcode_ele = cp.ele('css:.qrcode-img')
    qrcode_base64 = qrcode_ele.get_screenshot(as_base64=True)

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
        
    return return_data


def spider_jd(arg):
    cp = get_browser()

    cookies = arg['cookies']
    cp.set.cookies(cookies)

    cp.get('https://www.jd.com/')
    cp.ele('xpath://*[@id="key"]').input(arg['searchText'])
    cp.ele('xpath://*[@id="search"]/div/div[2]/button').click()
    cp.wait.load_start(timeout=5)
    cp.set.scroll.smooth(on_off=True)
    cp.scroll.to_bottom()
    cp.wait(1)
    cp.scroll.to_half()
    cp.wait(1)
    cp.scroll.to_top()
    cp.wait(1)

    items = cp.eles('xpath://li[@class="gl-item"]')
    return_data = []
    for item in items:
        id = item.attrs['data-sku']
        title = item('xpath://div[contains(@class,"p-name")]/a').text
        nick = item('xpath://a[@class="curr-shop hd-shopname"]').text
        item_url = item('xpath://div[contains(@class,"p-name")]/a').link
        img_url = item('xpath://div[contains(@class,"p-img")]/a/img').attrs['data-lazy-img']
        if img_url == "done":
            continue
        price = item('xpath://div[contains(@class,"p-price")]/strong/i').text
        item_data = {
            'real_id': id,
            'title': title,
            'item_url': item_url,
            'img_url': img_url,
            'price': price,
            'nick': nick,
            'procity': '',
            'specification': '',
            'type': 2
        }
        logger.info(item_data)
        return_data.append(item_data)
        print(id)
    return return_data


def price_history(domain, real_id):
    cp = get_browser()

    if domain == 'tmall':
        url = f'http://detail.tmallvvv.com/item.htm?id={real_id}'
    elif domain == 'jd':
        url = f'http://item.jdvvv.com/{real_id}.html'
    else:
        url = f'http://item.taobaovvv.com/item.htm?id={real_id}'
    cp.get(url)
    return_data = {}
    found = cp.ele('css:.flot-text', timeout=2)
    if found:
        canvas_element = cp.ele('@id=container')
        price_image = canvas_element.get_screenshot(as_base64=True)
        return_data['price_image'] = price_image
        return_data['OK'] = True
    else:
        return_data['OK'] = False
    return return_data


def get_tb_price(url, cookie):
    # cp = get_browser()
    # cp.set.cookies(cookie)
    # url = 'https:' + url
    # print(url)
    # cp.get(url)
    # price_ele = cp.ele('.^priceWrap')
    # price_text = price_ele.text
    # match = re.search(r'[-+]?\d*\.?\d+', price_text)
    # price_str = match.group(0)
    time.sleep(10)
    price = 51

    return price


def get_jd_price(url, cookie):
    cp = get_browser()
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
