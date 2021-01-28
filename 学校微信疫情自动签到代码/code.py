# @time     : 2021/1/267 10:55
# @Author   : Yt
# @FileName : code.py


import requests
import time
import random

id = ''  # 身份证
addr = ''  # 地址

# 选择是否推送server酱 默认关闭
server_j = '0'

# 填写server酱的sckey
sckey = '#'

# 随机生成体温
random_tw2 = random.randint(0, 7)


# 获取本地时间
def localtime():
    global now
    now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())


# 推送server
def push_wx():
    """
    推送消息到微信
    """

    text = '今日体温 36.{}'.format(random_tw2)
    server_url = "https://sc.ftqq.com/%s.send" % sckey
    params = {
        "text": text,
        "tw": random_tw2
    }

    response = requests.get(server_url, params=params)
    json_data = response.json()

    if json_data['errno'] == 0:
        print(localtime() + " 推送成功。")
    else:
        print("{0} 推送失败：{1} \n {2}".format(localtime(),
                                           json_data['errno'], json_data['errmsg']))


# 提交体温
def submit_tw():
    rq = requests.session()

    url = "http://fdcat.cn365vip.com/addu.php"

    headers = {
        'user-agent': 'Mozilla/5.0 (Linux; Android 10; Redmi Note 8 Pro Build/QP1A.190711.020; wv) AppleWebKit/537.36 (KHTML,'
                      ' like Gecko) Version/4.0 Chrome/77.0.3865.120 MQQBrowser/6.2 TBS/045511 Mobile Safari/537.36 MMWEBID/2857'
                      'rm64'}
    data = {'u_name': id,
            'upwd': '111111'}
    req = rq.post(url, data=data, headers=headers)

    url1 = "http://fdcat.cn365vip.com/adddt_s.php"

    # 随机生成体温
    random_tw2 = random.randint(0, 7)

    data_tw = {
        'u_addr': addr,
        'tw1': '36',
        'tw2': random_tw2,
        'cn': '1'
    }
    submit = rq.post(url1, data=data_tw, headers=headers)


def start():
    submit_tw()

    if server_j == '1':
        push_wx()


def main_handler(event, context):
    return start()


if __name__ == "__main__":
    start()
    print('今日体温 36.{}'.format(random_tw2))
