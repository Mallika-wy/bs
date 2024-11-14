import time

import DrissionPage.errors
from DrissionPage import ChromiumPage, ChromiumOptions
import re
import json
from bs4 import BeautifulSoup

from ..plugin import message_queue


def get_tb_cookies(name, password):
    co = ChromiumOptions()
    co = co.set_argument('--no-sandbox')  # 关闭沙箱模式, 解决`$DISPLAY`报错
    co = co.headless(True)
    cp = ChromiumPage(co)

    cp.get("https://login.taobao.com/member/login.jhtml")
    time.sleep(1)
    cp.ele('css:#fm-login-id').clear()
    cp.ele('css:#fm-login-id').input(name)
    cp.ele('css:#fm-login-password').clear()
    cp.ele('css:#fm-login-password').input(password)
    cp.ele('css:.fm-button.fm-submit.password-login').click()

    time.sleep(2)

    return_data = {}
    error_element = cp.ele('css:.login-error-msg', timeout=1)
    if error_element:
        return_data['OK'] = False
        cp.close()
        return return_data

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

    cp.quit()
    return return_data


def spider_taobao(arg):
    co = ChromiumOptions()
    co = co.set_argument('--no-sandbox')  # 关闭沙箱模式, 解决`$DISPLAY`报错
    co = co.headless(True)
    cp = ChromiumPage(co)

    cookies = arg['cookies']
    cp.set.cookies(cookies)

    cp.get('https://www.taobao.com/')
    cp.ele('css:#q').input(arg['searchText'])
    cp.ele('css:.btn-search.tb-bg').click()

    # cp.wait.load_start(timeout=2)
    # cp.scroll.to_bottom()
    # items = cp.eles('.=doubleCardWrapper')
    # for i in range(1, 49):
    #     xpath = f'xpath://*[@id="search-content-leftWrap"]/div[3]/div[3]/div/a[{i}]'
    #     item_ele = cp.ele(xpath)
    #     if item_ele is None:
    #
    #     item_url = item_ele.attr('href')
    #
    #     if 'tmall' in item_url:
    #         continue
    #
    #     item_ele = item_ele.ele('@tag()=div')
    #     sub_item1_ele = item_ele.ele('@tag()=div')
    #     sub_item2_ele = sub_item1_ele.next()
    #     sub_item3_ele = sub_item2_ele.next()
    #
    #     img_ele = sub_item1_ele.ele('@tag()=div')
    #     title_ele = img_ele.next()
    #     price_ele = title_ele.next(2)
    #
    #     img_ele = img_ele.ele('@tag()=img')
    #     img_url = img_ele.attr('src')
    #
    #     title = title_ele.ele('@tag()=div').text
    #
    #     price_ele = price_ele.ele('@tag()=div')
    #     price_string = price_ele.text
    #
    #     procity_ele = price_ele.next()
    #     print(1)
        # child_element = parent_element.xpath('.//div/div[1]')
        # //*[@id="search-content-leftWrap"]/div[3]/div[3]/div/a[37]/div/div[1]
    # items_ele = cp.ele('xpath://*[@id="search-content-leftWrap"]/div[3]/div[3]/div')
    # item1_ele = cp.ele('xpath://*[@id="search-content-leftWrap"]/div[3]/div[3]/div/a[1]')
    # //*[@id="search-content-leftWrap"]/div[3]/div[3]/div/a[1]
    # //*[@id="search-content-leftWrap"]/div[3]/div[3]/div/a[2]
    # //*[@id="search-content-leftWrap"]/div[3]/div[3]/div
    # return_data = []
    # for item in items:
    #     print(item)

        # id = item.attrs['data-sku']
        # title = item('xpath://div[contains(@class,"p-name")]/a').text
        # nick = item('xpath://a[@class="curr-shop hd-shopname"]').text
        # item_url = item('xpath://div[contains(@class,"p-name")]/a').link
        # img_url = item('xpath://div[contains(@class,"p-img")]/a/img').attrs['data-lazy-img']
        # price = item('xpath://div[contains(@class,"p-price")]/strong/i').text
        # item_data = {
        #     'real_id': id,
        #     'title': title,
        #     'item_url': item_url,
        #     'img_url': img_url,
        #     'price': price,
        #     'nick': nick,
        #     'procity': '',
        #     'specification': '',
        #     'type': 2
        # }
        # return_data.append(item_data)

    cp.listen.start('h5/mtop.relationrecommend.wirelessrecommend.recommend/2.0')
    response_list = cp.listen.wait(count=2)
    mtopjsonp = response_list[1].response.body
    mtopjson = re.findall('mtopjsonp\d+\((.*)\)', mtopjsonp)[0]
    mtop_data = json.loads(mtopjson)
    itemsArray = mtop_data['data']['itemsArray']

    return_data = []
    for item in itemsArray:
        soup = BeautifulSoup(item['title'], 'lxml')
        item['title'] = soup.get_text()

        # if 'tmall' in item['auctionURL']:
        #     item['price'] = -1
        #     continue

        item_data = {
            'real_id': item['item_id'],
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
    cp.quit()
    return return_data


def get_jd_qrcode_and_cookie():
    co = ChromiumOptions()
    co = co.set_argument('--no-sandbox')  # 关闭沙箱模式, 解决`$DISPLAY`报错
    co = co.headless(True)
    cp = ChromiumPage(co)
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

    cp.quit()
    return return_data


def spider_jd(arg):
    co = ChromiumOptions()
    co = co.set_argument('--no-sandbox')  # 关闭沙箱模式, 解决`$DISPLAY`报错
    co = co.headless(True)
    cp = ChromiumPage(co)

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
        return_data.append(item_data)
    cp.quit()
    return return_data


def price_history(domain, real_id):
    co = ChromiumOptions()
    co = co.set_argument('--no-sandbox')  # 关闭沙箱模式, 解决`$DISPLAY`报错
    co = co.headless(True)
    cp = ChromiumPage(co)

    if domain == 'tmall':
        url = f'http://detail.tmallvvv.com/item.htm?id={real_id}'
    elif domain == 'jd':
        url = f'http://item.jdvvv.com/{real_id}.html'
    else:
        url = f'http://item.taobaovvv.com/item.htm?id={real_id}'
    cp.get(url)
    time.sleep(2)
    return_data = {}
    not_found = cp.ele('@id=loadingId', timeout=2)
    if not_found:
        return_data['OK'] = False
    else:
        canvas_element = cp.ele('@id=container')
        price_image = canvas_element.get_screenshot(as_base64=True)
        return_data['price_image'] = price_image
        return_data['OK'] = True
    cp.close()
    return return_data


def get_tb_price(url, cookie):
    co = ChromiumOptions()
    co = co.set_argument('--no-sandbox')  # 关闭沙箱模式, 解决`$DISPLAY`报错
    co = co.headless(True)
    cp = ChromiumPage(co)
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
    co = ChromiumOptions()
    co = co.set_argument('--no-sandbox')  # 关闭沙箱模式, 解决`$DISPLAY`报错
    co = co.headless(True)
    cp = ChromiumPage(co)
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
