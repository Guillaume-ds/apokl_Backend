from django.db import models
from django.contrib.auth.models import User 
from django.contrib.postgres.fields import ArrayField

def user_directory_path(instance, filename):
    return f'photos/creator/{instance.name}/{filename}'.format(filename=filename)

class Creator(models.Model):
    user = models.ForeignKey(User, related_name="creator", on_delete=models.CASCADE,null=True, blank=True,unique=True)
    name = models.CharField(max_length=500,default='', blank=True)
    tags = ArrayField(models.CharField(max_length=200), blank=True, default=list)
    description = models.TextField(blank=True)
    picture = models.ImageField(upload_to=user_directory_path, default='', max_length=1000) 
    instagramUrl = models.CharField(max_length=500,default='', blank=True)
    twitterUrl = models.CharField(max_length=500,default='', blank=True)
    youtubeUrl = models.CharField(max_length=500,default='', blank=True)
    discordUrl = models.CharField(max_length=500,default='', blank=True)
    
    def __str__(self):
        return self.name
    

def collection_directory_path(instance, filename):
    return f'photos/collection/{instance.creator.name}/{filename}'.format(filename=filename)  

class Collection(models.Model):
    creator = models.ForeignKey(Creator, related_name="collections", on_delete=models.CASCADE,null=True, blank=True)
    slug = models.CharField(max_length=200, unique=True,default='Atest')
    name = models.CharField(max_length=200,default='')
    description = models.TextField(blank=True)
    tags = ArrayField(models.CharField(max_length=200), blank=True, default=list)
    nfts_array = ArrayField(models.CharField(max_length=200), blank=True, default=list)
    picture = models.ImageField(upload_to=collection_directory_path, default='', max_length=1000)
    def __str__(self):
        return self.name
    class Meta:
        ordering = ['-id']
    
     
