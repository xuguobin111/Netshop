
from django.db import models
from django.db.models import ForeignKey
class Area(models.Model):
    areaid = models.IntegerField(primary_key=True)
    areaname = models.CharField(max_length=50)
    parentid = models.IntegerField()
    arealevel = models.IntegerField()
    status = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'area'
class UserInfo(models.Model):
    uname=models.EmailField(max_length=20)
    pwd=models.CharField(max_length=60)
    def __unicode__(self):
        return u'<UserInfo:%s>'%self.uname
    class Meta:
        ordering=('id',)
class Address(models.Model):
    aname=models.CharField(max_length=30)
    aphone=models.CharField(max_length=11)
    addr=models.CharField(max_length=100)
    isdefault=models.BooleanField(default=False)
    userinfo=models.ForeignKey(UserInfo,on_delete=models.CASCADE)





