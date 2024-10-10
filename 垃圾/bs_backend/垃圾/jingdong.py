import random

from DrissionPage import ChromiumPage
import time
import re
import json
import ddddocr
import base64
from PIL import Image
import io


def get_track7(distance):
    """
    根据偏移量和手动操作模拟计算移动轨迹
    :param distance: 偏移量
    :return: 移动轨迹
    """
    # 移动轨迹
    tracks = []
    # 当前位移
    current = 0
    # 减速阈值
    mid = distance * 4 / 5
    # 时间间隔
    t = 0.2
    # 初始速度
    v = 0

    while current < distance:
        if current < mid:
            a = random.uniform(2, 5)
        else:
            a = -(random.uniform(12.5, 13.5))
        v0 = v
        v = v0 + a * t
        x = v0 * t + 1 / 2 * a * t * t
        current += x

        if 0.6 < current - distance < 1:
            x = x - 0.53
            tracks.append(round(x, 2))

        elif 1 < current - distance < 1.5:
            x = x - 1.4
            tracks.append(round(x, 2))
        elif 1.5 < current - distance < 3:
            x = x - 1.8
            tracks.append(round(x, 2))

        else:
            tracks.append(round(x, 2))

    print(sum(tracks))
    return tracks


def get_jd_cookies(name, password):
    cp = ChromiumPage()
    cp.get("https://passport.jd.com/new/login.aspx")
    cp.ele('css:#loginname').clear()
    cp.ele('css:#loginname').input(name)
    cp.ele('css:#nloginpwd').clear()
    cp.ele('css:#nloginpwd').input(password)
    cp.ele('css:#loginsubmit').click()
    time.sleep(1)

    bg_element = cp.ele('xpath://*[@id="JDJRV-wrap-loginsubmit"]/div/div/div/div[1]/div[2]/div[1]/img')
    time.sleep(2)
    bg_base64 = bg_element.attr('src').split("base64,")[1]
    bg_bytes = base64.b64decode(bg_base64)
    bg_image = Image.open(io.BytesIO(bg_bytes))
    bg_image.save('bg.png', 'png')

    cut_element = cp.ele('xpath://*[@id="JDJRV-wrap-loginsubmit"]/div/div/div/div[1]/div[2]/div[2]/img')
    time.sleep(2)
    cut_base64 = cut_element.attr('src').split("base64,")[1]
    cut_bytes= base64.b64decode(cut_base64)
    cut_image = Image.open(io.BytesIO(cut_bytes))
    cut_image.save('cut.png', 'png')

    det = ddddocr.DdddOcr(det=False, ocr=False, show_ad=False)
    result = det.slide_match(cut_bytes, bg_bytes, simple_target=True)
    offset = result['target'][0]
    offset = offset*343/360
    print("offset: ", offset)

    # number_list = 0
    # duration = 0
    # if offset < 50:
    #     number_list = 75
    #     duration = 2
    # elif offset < 100:
    #     number_list = 100
    #     duration = 3
    # elif offset < 200:
    #     number_list = 150
    #     duration = 2
    # elif offset < 300:
    #     number_list = 200
    #     duration = 2.5
    # else:
    #     number_list = 250
    #     duration = 5
    #
    # bezier_trajectory = BezierTrajectory()
    # trace_dict = bezier_trajectory.trackArray(start=[0, 0], end=[offset, 0], numberList=number_list, deviation=5, type=2, cbb=2)
    # trace_np = trace_dict['trackArray']
    # trace_x_np = trace_np[:, 0]
    # trace_x_list = [round(x) for x in trace_x_np]
    # trace_x_list = [trace_x_list[i + 1] - trace_x_list[i] for i in range(len(trace_x_list) - 1)]
    #
    # cp.actions.hold('css:.JDJRV-slide-inner.JDJRV-slide-btn')
    #
    # for trace in trace_x_list:
    #     cp.actions.move(offset_x=trace, offset_y=round(random.uniform(0, 20)), duration=duration/number_list)

    cp.actions.hold('css:.JDJRV-slide-inner.JDJRV-slide-btn')
    tracks = get_track7(offset)
    for track in tracks:
        cp.actions.move(offset_x=track, offset_y=round(random.uniform(0, 20)), duration=1 / len(tracks))
    time.sleep(0.18)
    cp.actions.move(offset_x=-3, offset_y=round(random.uniform(0, 20)), duration=0.1)
    cp.actions.move(offset_x=3, offset_y=round(random.uniform(0, 20)), duration=0.1)
    time.sleep(0.7)

    cp.actions.release('css:.JDJRV-slide-inner.JDJRV-slide-btn')
    time.sleep(30)
    cookies = cp.cookies()
    return cookies


def spider_jd(arg):
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

    return qrcode_url


if __name__ == '__main__':
    # tracks = get_track7(200)
    # print(tracks)
    get_jd_cookies('18205098642', '2004wangyang')


