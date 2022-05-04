from django.db import models
from register_login.models import User

# Create your models here.
# class Notes(models.Model):
#     title = models.CharField('标题',max_length=100)
#     content = models.TextField('内容')
#     created_time = models.DateTimeField('创建时间',auto_now_add=True)
#     update_time = models.DateTimeField('更新时间',auto_now_add=True)
#     user = models.ForeignKey(User,on_delete=models.CASCADE)#因为一个作者可能有多个笔记，是一对多的关系，这里设置外键关联User表
