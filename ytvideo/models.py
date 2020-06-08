from django.db import models


# Create your models here.
class Comment(models.Model):
    # 所属视频的av号
    oid = models.BigIntegerField()
    # 用户的id
    mid = models.BigIntegerField(null=True)

    root = models.BigIntegerField(default=0)
    parent = models.BigIntegerField(default=0)

    # 回复id
    rpid = models.BigIntegerField(primary_key=True)
    # 用户名
    username = models.CharField(max_length=512, null=True)
    # 性别
    gender = models.CharField(max_length=32, null=True)
    # 创建时间
    ctime = models.BigIntegerField(null=True)
    # 评论内容
    content = models.CharField(max_length=4096, null=True)
    # 点赞数
    likes = models.SmallIntegerField(null=True)
    # 被回复数
    rcounts = models.SmallIntegerField(null=True)
