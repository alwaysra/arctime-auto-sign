# coding:utf-8

'''
Arctime账户自动签到
作者：雪山凌狐
日期：2020-05-11
版本号：1.0
网址：http://www.xueshanlinghu.com

Arctime账户每天签到可以获得20积分（1元=100积分，即每日可以得0.2元。可以用于购买增值服务等），我们来写个自动化脚本吧！
'''

import requests
import sys

init_login_url = "http://m.arctime.cn/home/user/login.html"
login_url = "http://m.arctime.cn/home/user/login_save.html"
ucenter_url = "http://m.arctime.cn/home/ucenter/index.html"
sign_url = "http://m.arctime.cn/home/ucenter/attendance.html"

def init_login():
    headers = {
        'Host': 'm.arctime.cn',
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3314.0 Safari/537.36 SE 2.X MetaSr 1.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Referer': 'http://m.arctime.cn/home/ucenter/index.html'
    }
    res = requests.get(init_login_url, headers=headers)
    if res.status_code == 200:
        res.encoding = 'utf-8'
        print("获取cookies成功")
        print(res.cookies)
        return res.cookies
    else:
        return None

def login():
    headers = {
        'Host': 'm.arctime.cn',
        'Connection': 'keep-alive',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'X-Requested-With': 'XMLHttpRequest',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3314.0 Safari/537.36 SE 2.X MetaSr 1.0',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Referer': 'http://m.arctime.cn/home/user/login.html'
    }
    body = "username=%s&password=%s&login_type=2" % (username, password)
    res = requests.post(login_url, data=body, headers=headers, cookies=cookies)
    if res.status_code == 200:
        res.encoding = "utf-8"
        content = res.json()
        if content.get("msg") == "登录成功":
            print("登录成功！")
            return True
        else:
            return False

def getmidstring(html, start_str, end):
    start = html.find(start_str)
    if start >= 0:
        start += len(start_str)
        end = html.find(end, start)
        if end >= 0:
            return html[start:end].strip()

def auto_sign():
    headers = {
        'Host': 'm.arctime.cn',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3314.0 Safari/537.36 SE 2.X MetaSr 1.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Referer': 'http://m.arctime.cn/home/user/login.html'
    }
    res = requests.get(ucenter_url, headers=headers, cookies=cookies)
    if res.status_code == 200:
        res.encoding = 'utf-8'
        content = res.text
        # 获取现有积分
        points = getmidstring(content, "共获得", "积分")
        print("您目前拥有的积分为：%s" % points)
        if content.find("立即签到领取积分") > -1:
            headers = {
                'Host': 'm.arctime.cn',
                'Connection': 'keep-alive',
                'Accept': 'application/json, text/javascript, */*; q=0.01',
                'X-Requested-With': 'XMLHttpRequest',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3314.0 Safari/537.36 SE 2.X MetaSr 1.0',
                'Referer': 'http://m.arctime.cn/home/ucenter/index.html'
            }
            body = " "
            res = requests.post(sign_url, data=body, headers=headers, cookies=cookies)
            if res.status_code == 200:
                res.encoding = "utf-8"
                content = res.json()
                print(content.get("msg"))
        elif content.find("今日已经签到") > -1:
            print("您今天已经签到过了")
        else:
            print("未知报错，请检查程序或联系作者！")
    else:
        print("访问用户个人中心页面失败")

if __name__ == '__main__':
    if len(sys.argv) != 3:
        raise Exception("传入参数不正确，第一个传入参数为登入的账号，第二个传入账户为密码")

    username = sys.argv[1]
    password = sys.argv[2]

    # 初始化登录，获取cookies
    cookies = init_login()
    if cookies:
        # 登录
        res = login()
        if res:
            # 检测并自动签到
            auto_sign()
        else:
            print("登录失败！")
    else:
        print("初始化失败！")