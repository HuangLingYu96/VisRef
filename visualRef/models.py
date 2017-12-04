from django.db import models

# Create your models here.
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
    star_title=models.CharField(max_length=500)
    star_source=models.CharField(max_length=100)
    star_time=models.DateField()

    def __str__(self):
        return self.username+'+'+self.star_doi