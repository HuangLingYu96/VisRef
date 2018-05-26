from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

#记录doi与对应的文件代号
class File(models.Model):
    doi=models.CharField(max_length=100)

#记录已请求的ref doi
class Ref(models.Model):
    ref_doi = models.CharField(max_length=100)
    create_rtime = models.DateField()

    def __str__(self):
        return self.ref_doi

#记录已请求过的cit doi
class Cit(models.Model):
    cit_doi=models.CharField(max_length=100)
    create_ctime=models.DateField()

    def __str__(self):
        return self.cit_doi

#记录已请求过的sum doi
class Sum(models.Model):
    sum_doi=models.CharField(max_length=100)
    create_stime=models.DateField()

    def __str__(self):
        return self.sum_doi

#记录用户的star
class Star(models.Model):
    username=models.CharField(max_length=100)
    star_doi=models.CharField(max_length=100)
    star_file=models.CharField(max_length=100)
    star_title=models.CharField(max_length=500)
    star_source=models.CharField(max_length=100)
    star_time=models.DateField()

    def __str__(self):
        return self.username+'+'+self.star_doi

#分页类
class Pagination(models.Model):
    def toJSON(self):
        fields = []
        for field in self._meta.fields:
            fields.append(field.name)

        d = {}
        import datetime
        for attr in fields:
            if isinstance(getattr(self, attr), datetime.datetime):
                d[attr] = getattr(self, attr).strftime('%Y-%m-%d %H:%M:%S')
            elif isinstance(getattr(self, attr), datetime.date):
                d[attr] = getattr(self, attr).strftime('%Y-%m-%d')
            else:
                d[attr] = getattr(self, attr)

        import json
        return json.dumps(d)

#search类
class Sea(models.Model):
    keyword=models.CharField(max_length=100)
    doi=models.CharField(max_length=100)
    link=models.CharField(max_length=500)
    sea_type=models.CharField(max_length=100)
    time=models.CharField(max_length=100)
    publisher=models.CharField(max_length=100)
    volume=models.CharField(max_length=100)
    issue=models.CharField(max_length=100)
    page_from=models.CharField(max_length=100)
    page_to=models.CharField(max_length=100)
    title=models.CharField(max_length=500)
    author=models.CharField(max_length=3000)

#自定义的user模型profile
class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    bio=models.TextField(max_length=500,blank=True)
    company=models.CharField(max_length=100,blank=True)
    loaction = models.CharField(max_length=100, blank=True)
    birth_date = models.DateField(null=True, blank=True)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

#信息表
class Info(models.Model):
    doi = models.CharField(max_length=100)
    link = models.CharField(max_length=500)
    type = models.CharField(max_length=100)
    time = models.CharField(max_length=100)
    container_title = models.CharField(max_length=100)
    page= models.CharField(max_length=100)
    title = models.CharField(max_length=500)
    author = models.CharField(max_length=3000)
    is_referenced_by_count=models.CharField(max_length=100)
    reference_count = models.CharField(max_length=100)