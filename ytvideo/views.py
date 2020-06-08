import random

from django.shortcuts import render

from .models import Comment
from .comment_api import *
from django.http import HttpResponse, HttpResponseRedirect


# Create your views here.
def get_comments(request):
    http_response = "You Should Enter An OID"
    if request.GET.get('oid') is not []:
        # print(request.GET.get('oid'))
        oid = request.GET.get('oid')
        http_response = oid

    url = 'https://api.bilibili.com/x/v2/reply?type=1&oid=' + oid
    html = fetch_url(url)

    pages = get_pages(oid)

    replies = []

    print("共", pages, "页")

    for i in range(pages):
        replies_cur_page = parse_html(fetch_url(form_url(oid=oid, page=i)))
        for reply in replies_cur_page:
            replies.append(reply)

    comments = []
    for reply in replies:
        # mid, floor, username, gender, ctime, content, likes, rcounts, rpid
        comment = Comment(mid=reply['mid'], username=reply['member']
        ['uname'], gender=reply['member']['sex'], ctime=reply['ctime'],
                          content=reply['content']['message'], likes=reply['like'],
                          rcounts=reply['rcount'], rpid=reply['rpid'], root=reply['root'], parent=reply['parent'],
                          oid=oid)
        comments.append(comment)
        if reply['rcount'] > 0:
            for item in reply['replies']:
                comment = Comment(mid=item['mid'], username=item['member']
                ['uname'], gender=item['member']['sex'], ctime=item['ctime'],
                                  content=item['content']['message'], likes=item['like'],
                                  rcounts=item['rcount'], rpid=item['rpid'], root=reply['root'], parent=reply['parent'],
                                  oid=oid)
                comments.append(comment)

    print(comments)

    for item in comments:
        item.save()
        http_response = "视频：" + str(oid) + "的评论更新成功"

    return HttpResponse(http_response)


def print_comment(comm):
    return ("|[B站ID]:" + str(comm.mid) + "|[昵称]:" + str(comm.username) + "|[评论ID]:" + str(comm.rpid) + "|[性别]:" +
            str(comm.gender) + "|[评论内容]:" + str(comm.content) + "|[评论时间]:" + str(comm.ctime) + "|[点赞数]:" + str(
                comm.likes) + '<br />')


def lottery(request):
    http_response = ""

    if request.GET.get('oid') is not []:
        oid = request.GET.get('oid')
    if request.GET.get('num') is not []:
        num = int(request.GET.get('num'))

    comments = Comment.objects.filter(oid=oid)
    comment_list = []

    print("共有", len(comments), "条评论")

    for comm in comments:
        if not check_user_exist(comm, comment_list):
            comment_list.append(comm)

    print("清理掉重复评论", len(comments) - len(comment_list), "条")

    bingo = []

    for i in range(num):
        tmp_rand = random.randint(0, len(comment_list))
        print(tmp_rand)
        while tmp_rand in bingo:
            print(tmp_rand)
            tmp_rand = random.randint(0, len(comment_list))
        bingo.append(tmp_rand)

    for i in bingo:
        http_response += print_comment(comment_list[i])

    return HttpResponse(http_response)
