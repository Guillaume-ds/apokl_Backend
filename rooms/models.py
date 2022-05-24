from django.db import models
from django.contrib.postgres.fields import ArrayField
from creators.models import Collection,Creator


def room_directory_path(instance, filename):
  name= instance.creator.name
  return f'photos/room/{name}/{filename}'.format(filename=filename) 

class Room(models.Model):
  title = models.CharField(max_length=255)
  content = models.TextField()
  creator = models.ForeignKey(Creator, on_delete=models.CASCADE, related_name='rooms',blank=True, null=True)
  collection = models.ForeignKey(Collection, on_delete=models.CASCADE, related_name='rooms',blank=True, null=True)
  addresses= ArrayField(models.CharField(max_length=10000), blank=True, default=list)
  users= ArrayField(models.CharField(max_length=10000), blank=True, default=list)
  picture2 = models.ImageField(upload_to=room_directory_path, default='', max_length=2000, blank=True)
  picture = models.ImageField(upload_to=room_directory_path, default='', max_length=2000, blank=True)
  def __str__(self):
    return self.title
  class Meta:
        ordering = ['-id']
	
def post_directory_path(instance, filename):
  name=hash(instance.creator.name)
  return f'photos/post/{name}/{filename}'.format(filename=filename) 
  
class Post(models.Model):
  title = models.CharField(max_length=255)
  content = models.TextField(blank=True, null=True)
  creator = models.ForeignKey(Creator, on_delete=models.CASCADE, related_name='posts',blank=True, null=True)
  collection = models.ForeignKey(Collection, on_delete=models.CASCADE, related_name='posts',blank=True, null=True)
  picture = models.ImageField(upload_to=post_directory_path, default='', max_length=2000, blank=True)
  picture2 = models.ImageField(upload_to=post_directory_path, default='', max_length=2000, blank=True)
  def __str__(self):
    return self.title
  class Meta:
        ordering = ['-id']
        
class Comment(models.Model):
  content = models.TextField(blank=True, null=True)
  creator = models.ForeignKey(Creator, on_delete=models.CASCADE, related_name='comment',blank=True, null=True)
  post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comment',blank=True, null=True)
  class Meta:
        ordering = ['-id']