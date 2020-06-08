import requests
import json

import math


def fetch_url(url):
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
    }

    try:
        r = requests.get(url, headers=headers)
        r.raise_for_status()
        print(r.url)
        return r.text
    except requests.HTTPError as e:
        print(e)
        print("HTTPError")
    except requests.RequestException as e:
        print(e)
    except:
        print("Unknown Error !")


def parse_html(html):
    s = json.loads(html)

    reply_list = []
    reply_list = s['data']['replies']
    return reply_list


def form_url(oid, page):
    base_url = 'https://api.bilibili.com/x/v2/reply?type=1&'
    return base_url + 'oid=' + str(oid) + '&pn=' + str(page)


def get_pages(oid):
    base_url = 'https://api.bilibili.com/x/v2/reply?type=1&oid='
    html = fetch_url(base_url + str(oid))
    data = json.loads(html)['data']
    pages = math.ceil(data['page']['count'] / data['page']['size'])
    return pages


def check_exist_comment(comm, comms):
    existed = False
    for item in comms:
        if item.rpid == comm.rpid:
            existed = True
    return existed


# 检查该用户的评论是否已经存在
def check_user_exist(comm, comm_list):
    existed = False
    for item in comm_list:
        if comm.mid == item.mid:
            existed = True
    return existed
