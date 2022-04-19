from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from creators.models import Collection

def upload_to(instance, filename):
    return 'images/{filename}'.format(filename=filename)

class Room(models.Model):
  title = models.CharField(max_length=255)
  content = models.TextField()
  creator = models.ForeignKey(User, on_delete=models.CASCADE)
  adresses= ArrayField(models.CharField(max_length=10000), blank=True, default=list)
  users= ArrayField(models.CharField(max_length=10000), blank=True, default=list)
  picture2 = models.ImageField(upload_to=f'photos/rooms/{creator}', default='', max_length=1000)
  picture = models.ImageField(upload_to=f'photos/rooms/{creator}', default='', max_length=1000)
  def __str__(self):
    return self.title
	

class Post(models.Model):
  title = models.CharField(max_length=255)
  content = models.TextField()
  creator = models.ForeignKey(User, on_delete=models.CASCADE)
  collection = models.ForeignKey(Collection, on_delete=models.CASCADE, related_name='posts')
  picture = models.ImageField(upload_to=f'photos/rooms/posts/{creator}', default='', max_length=1000)
  picture2 = models.ImageField(upload_to=f'photos/rooms/posts/{creator}', default='', max_length=1000)
  def __str__(self):
    return self.title