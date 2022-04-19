from django.db import models
from django.contrib.postgres.fields import ArrayField

def upload_to(instance, filename):
    return 'images/{filename}'.format(filename=filename)

class Creator(models.Model):
    name = models.CharField(max_length=200,unique=True)
    tags = ArrayField(models.CharField(max_length=200), blank=True, default=list)
    picture = models.ImageField(upload_to=f'photos/creator/{name}', default='', max_length=1000) 
    instagramUrl = models.CharField(max_length=500,default='')
    twitterUrl = models.CharField(max_length=500,default='')
    youtubeUrl = models.CharField(max_length=500,default='')
    discordUrl = models.CharField(max_length=500,default='')
    def __str__(self):
        return self.name
    class Meta:
        ordering = ['-id']
       

class Collection(models.Model):
    creator = models.CharField(max_length=200,default='')
    slug = models.CharField(max_length=200, unique=True,default='Atest')
    name = models.CharField(max_length=200,default='')
    description = models.TextField(blank=True)
    tags = ArrayField(models.CharField(max_length=200), blank=True, default=list)
    nfts = ArrayField(models.CharField(max_length=200), blank=True, default=list)
    picture = models.ImageField(upload_to=f'photos/collection/{name}_{slug}', default='', max_length=1000)
    def __str__(self):
        return self.name
    class Meta:
        ordering = ['-id']
    
     
