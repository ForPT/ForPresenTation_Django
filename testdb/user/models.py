from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.
class User(models.Model):
    status = models.CharField(default='logined', max_length=64, verbose_name='로그인상태')
    userid = models.CharField(default ='', max_length=64, verbose_name='학번')
    username = models.CharField(max_length=64,verbose_name='사용자명')
    password = models.CharField(max_length=64,verbose_name='비밀번호')
    registered_dttm = models.DateTimeField(auto_now_add=True,verbose_name='등록시간')
    managed_room = models.CharField(default='', max_length=64, verbose_name='관리중')#여러개일수잇음(ex. 정통개/신시)
    joined_room = models.CharField(default='', max_length=64, verbose_name='참여중') #여러개일수있음(ex. 정통개/신시)

    def __str__(self):
        return self.userid

    class Meta:
        db_table = 'test_user'

class Room(models.Model):
    participant = models.IntegerField(default=0, null=True)
    limit = models.CharField(default='', null= True, max_length=64)
    room_name = models.CharField(default = '', null = True, max_length=64)
    professor = models.CharField(default = '' , null = True, max_length=64) 
    student = models.CharField(default = '', null = True, max_length=64)
    # page = models.IntegerField(default=0, null=True)
    page = models.CharField(default=0, null=True, max_length=64)
    temp_page = models.IntegerField(default=0, null=True)
    def __str__(self):
        return self.room_name

    def __int__(self):
        self.page+=1
        return self.page    
        
    class Meta:
        db_table = 'test_room' 
#add from youtube : https://www.youtube.com/watch?v=KQJRwWpP8hs
#http://3.34.253.194:8000/media/files/ppts/201700000_교양영어_1.png
def file_name(instance, filename):
    return 'files/ppts/{}_{}_{}.png'.format(instance.number, instance.entered_room, instance.page)
   
class File(models.Model):
    time = models.DateTimeField(null=True, auto_now_add=True)
    number = models.CharField(default ='' , null = True, max_length=64)
    name = models.CharField(default ='' , null = True, max_length=64)
    comment = models.CharField(default ='' , null = True, max_length=255)
    page = models.IntegerField(default=0, null=True)
    ppt = models.FileField(upload_to=file_name)
    #https://stackoverflow.com/questions/1190697/django-filefield-with-upload-to-determined-at-runtime?rq=1
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, blank=True, null=True)
    entered_room = models.CharField(default='', null=True, max_length=64)
    def __str__(self):
        self.page = self.page + 1 
        return self.number
    class Meta:
        db_table = 'test_file'  